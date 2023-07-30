from flask import *
import os
from werkzeug.utils import secure_filename
from database import *
import uuid
from mutagen.mp3 import MP3
import random
from genre_rec_service import Genre_Recognition_Service
from pydub import AudioSegment
from analytics import *
from deletion import *
from other_processing import *
uploader =Blueprint('uploader',__name__)

@uploader.route('/')
def home():
    if 'uid' in session:
        uid = session['uid']
        data = {}
        count={}
        q="SELECT COUNT(song_id) AS song_count FROM songs WHERE user_id=%s"% (uid)
        song_count=select(q)
        q="SELECT COUNT(album_id) AS album_count FROM album WHERE user_id=%s"% (uid)
        album_count=select(q)
        q="SELECT COUNT(artist_id) AS artist_count FROM artist WHERE user_id=%s"% (uid)
        artist_count=select(q)
        data = {
            'counts': {
                'song_count': song_count[0]['song_count'],
                'album_count': album_count[0]['album_count'],
                'artist_count': artist_count[0]['artist_count']
            }
        }
        login_id = session['login_id']
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        q="SELECT s.song_id, s.song_name, IFNULL(al.album_name, 'No album') AS album_name, IFNULL(GROUP_CONCAT(ar.artist_name SEPARATOR ', '), 'No artist') AS artist_name, s.date, s.status, s.privacy FROM songs s LEFT JOIN songartist sar USING (song_id) LEFT JOIN artist ar ON ar.artist_id = sar.artist_id LEFT JOIN album al USING (album_id) WHERE s.user_id = '%s' GROUP BY s.song_id ORDER BY song_id DESC LIMIT 10"%(uid)
        recentsongdata=select(q) #last 10 songs
        data['recentsongdata']=recentsongdata
        q="SELECT DATE(TIMESTAMP) AS dates, COUNT(*) AS clicks FROM clicks c WHERE (content_type = 'song' AND EXISTS (SELECT 1 FROM songs s WHERE s.song_id = c.content_id AND s.user_id = '%s')) OR (content_type = 'album' AND EXISTS (SELECT 1 FROM album a WHERE a.album_id = c.content_id AND a.user_id = '%s')) OR (content_type = 'artist' AND EXISTS (SELECT 1 FROM artist ar WHERE ar.artist_id = c.content_id AND ar.user_id = '%s')) GROUP BY DATE(TIMESTAMP)"%(uid,uid,uid)
        totalclicks=select(q)
        clicks, dates = getClicksDatesInc(totalclicks)
        data['chartdata']={'clicks':clicks,'dates':dates}
        q="SELECT 'Songs' AS name,COUNT(c.content_type) AS clicks FROM clicks c INNER JOIN songs s ON c.content_id=s.song_id AND c.content_type='song' AND s.user_id='%s' GROUP BY name UNION SELECT 'Albums' AS name,COUNT(c.content_type) AS clicks FROM clicks c INNER JOIN album a ON c.content_id=a.album_id AND c.content_type='album' AND a.user_id='%s' GROUP BY name UNION SELECT 'Artists' AS name,COUNT(c.content_type) AS clicks FROM clicks c INNER JOIN artist a ON c.content_id=a.artist_id AND c.content_type='artist' AND a.user_id='%s' GROUP BY name"%(uid,uid,uid)
        clickdata=select(q)
        return render_template('uploader/home.html', data=data,count=count,clickdata=clickdata)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@uploader.route('/allsongs' , methods=['GET', 'POST'])
def allsongs():
    if 'uid' in session:
        uid = session['uid']
        login_id = session['login_id']
        q="update notification set status='read' where (notification_type = 'approvals' OR notification_type = 'songremoval') and user_id='%s'"%(login_id)
        update(q)
        data = {}
        count={}
        login_id = session['login_id']
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        q="SELECT s.song_id, s.song_name, IFNULL(al.album_name, 'No album') AS album_name, IFNULL(GROUP_CONCAT(ar.artist_name SEPARATOR ', '), 'No artist') AS artist_name, s.date, s.status, s.privacy FROM songs s LEFT JOIN songartist sar USING (song_id) LEFT JOIN artist ar ON ar.artist_id = sar.artist_id LEFT JOIN album al USING (album_id) WHERE s.user_id = '%s' GROUP BY s.song_id;"%(uid)
        allsongdata=select(q)
        data['allsongdata']=allsongdata
        q="select * from artist"
        artistdata=select(q)
        data['artistdata'] = artistdata
        q="select * from album"
        albumdata=select(q)
        data['albumdata']=albumdata
        data['currentsongdata']=0
        if request.method == 'POST':
            action = request.form.get('action')
            song_id = action.split('_')[-1]
            q="SELECT s.song_id, s.song_name, al.album_id, IFNULL(al.album_name, 'Null') AS album_name, IFNULL(GROUP_CONCAT(ar.artist_name SEPARATOR ', '), 'Null') AS artist_name, s.date, s.image_loc, s.song_loc, s.genre, s.language, s.privacy FROM songs s LEFT JOIN songartist sar USING (song_id) LEFT JOIN artist ar ON ar.artist_id = sar.artist_id LEFT JOIN album al USING (album_id) WHERE s.song_id = '%s' GROUP BY s.song_id"%(song_id)
            currentsongdata=select(q)
            data['currentsongdata']=currentsongdata[0]
            q="SELECT artist_id, artist_name FROM artist INNER JOIN songartist USING (artist_id) WHERE song_id='%s'"%(song_id)
            currentartistdata=select(q)
            data['currentartistdata']=currentartistdata
            if action.startswith('update_song'):
                return render_template('uploader/all_songs.html', data=data,count=count, value='updatesong')
            elif action.startswith('view_song'):
                 return render_template('uploader/all_songs.html', data=data,count=count, value='viewsong')
            elif action.startswith('delete_song'):
                message = songDeletion(song_id)
                flash(message)
                return redirect(url_for('uploader.allsongs'))
        return render_template('uploader/all_songs.html', data=data,count=count)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@uploader.route('/approvedsongs' , methods=['GET', 'POST'])
def approvedsongs():
    if 'uid' in session:
        uid = session['uid']
        login_id = session['login_id']
        data = {}
        count={}
        q="update notification set status='read' where (notification_type = 'approvals' OR notification_type = 'songremoval') and user_id='%s'"%(login_id)
        update(q)
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        q="SELECT s.song_id, s.song_name, COALESCE(al.album_name, 'No album') AS album_name, COALESCE(GROUP_CONCAT(ar.artist_name SEPARATOR ', '), 'No artist') AS artist_name, s.date, s.status, s.privacy FROM songs s LEFT JOIN songartist sar ON s.song_id = sar.song_id LEFT JOIN artist ar ON ar.artist_id = sar.artist_id LEFT JOIN album al ON al.album_id = s.album_id WHERE s.privacy = 'public' AND s.status = 'approved' AND s.user_id = '%s' GROUP BY s.song_id"%(uid)
        approvedsongdata=select(q)
        data['approvedsongdata']=approvedsongdata
        q="select * from artist"
        artistdata=select(q)
        data['artistdata'] = artistdata
        q="select * from album"
        albumdata=select(q)
        data['albumdata']=albumdata
        data['currentsongdata']=0
        if request.method == 'POST':
                action = request.form.get('action')
                song_id = action.split('_')[-1]
                q="SELECT s.song_id, s.song_name, al.album_id, COALESCE(al.album_name, 'Null') AS album_name, COALESCE(GROUP_CONCAT(ar.artist_name SEPARATOR ', '), 'Null') AS artist_name, s.date, s.image_loc, s.song_loc, s.genre, s.language, s.privacy FROM songs s INNER JOIN songartist sar USING (song_id) LEFT JOIN artist ar ON ar.artist_id = sar.artist_id LEFT JOIN album al USING (album_id) WHERE s.song_id = '%s' GROUP BY s.song_id;"%(song_id)
                currentsongdata=select(q)
                data['currentsongdata']=currentsongdata[0]
                q="SELECT artist_id, artist_name FROM artist INNER JOIN songartist USING (artist_id) WHERE song_id='%s'"%(song_id)
                currentartistdata=select(q)
                data['currentartistdata']=currentartistdata
                if action.startswith('update_song'):
                    return render_template('uploader/approved_songs.html', data=data,count=count, value='updatesong')
                elif action.startswith('view_song'):
                    return render_template('uploader/approved_songs.html', data=data,count=count, value='viewsong')
                elif action.startswith('delete_song'):
                    message = songDeletion(song_id)
                    flash(message)
                    return redirect(url_for('uploader.approvedsongs'))

        return render_template('uploader/approved_songs.html', data=data,count=count)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@uploader.route('/pendingsongs' , methods=['GET', 'POST'])
def pendingsongs():
    if 'uid' in session:
        uid = session['uid']
        login_id = session['login_id']
        data = {}
        count={}
        login_id = session['login_id']
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        q="SELECT s.song_id, s.song_name, al.album_name, GROUP_CONCAT(ar.artist_name SEPARATOR ', ') AS artist_name, s.date, s.status,s.privacy FROM songs s INNER JOIN songartist sar USING (song_id) INNER JOIN artist ar ON ar.artist_id = sar.artist_id INNER JOIN album al USING (album_id) WHERE s.privacy='public' and s.status='pending' and s.user_id='%s' GROUP BY s.song_id;"%(uid)
        pendingsongdata=select(q)
        data['pendingsongdata']=pendingsongdata
        q="select * from artist"
        artistdata=select(q)
        data['artistdata'] = artistdata
        q="select * from album"
        albumdata=select(q)
        data['albumdata']=albumdata
        data['currentsongdata']={}
        data['currentartistdata']={}
        if request.method == 'POST':
                action = request.form.get('action')
                song_id = action.split('_')[-1]
                q="SELECT s.song_id,s.song_name,al.album_id,al.album_name,GROUP_CONCAT(ar.artist_name SEPARATOR ', ') AS artist_name,s.date,s.image_loc,s.song_loc,s.genre,s.language,s.privacy FROM songs s INNER JOIN songartist sar USING (song_id) INNER JOIN artist ar ON ar.artist_id=sar.artist_id INNER JOIN album al USING (album_id) where s.song_id='%s' GROUP BY s.song_id"%(song_id)
                currentsongdata=select(q)
                q="SELECT artist_id, artist_name FROM artist INNER JOIN songartist USING (artist_id) WHERE song_id='%s'"%(song_id)
                currentartistdata=select(q)
                data['currentsongdata']=currentsongdata[0]
                data['currentartistdata']=currentartistdata
                if action.startswith('update_song'):
                    return render_template('uploader/pending_songs.html', data=data,count=count, value='updatesong')
                elif action.startswith('view_song'):
                    return render_template('uploader/pending_songs.html', data=data,count=count, value='viewsong')
                elif action.startswith('delete_song'):
                    message = songDeletion(song_id)
                    flash(message)
                    return redirect(url_for('uploader.pendingsongs'))
        return render_template('uploader/pending_songs.html', data=data,count=count)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@uploader.route('/rejectedsongs')
def rejectedsongs():
    if 'uid' in session:
        uid = session['uid']
        login_id = session['login_id']
        data = {}
        count={}
        login_id = session['login_id']
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        q="SELECT s.song_id, s.song_name, al.album_name, GROUP_CONCAT(ar.artist_name SEPARATOR ', ') AS artist_name, s.date, s.status,s.privacy FROM songs s INNER JOIN songartist sar USING (song_id) INNER JOIN artist ar ON ar.artist_id = sar.artist_id INNER JOIN album al USING (album_id) WHERE s.user_id='%s' and s.status='rejected' GROUP BY s.song_id;"%(uid)
        rejectedsongdata=select(q)
        data['rejectedsongdata']=rejectedsongdata
        return render_template('uploader/rejected_songs.html', data=data,count=count)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))
    
@uploader.route('/updatesong' , methods=['GET', 'POST'])
def updatesong():
    if request.method == 'POST':
        if 'uploadimage' in request.form:
            songname=request.form['songname']
            songid=request.form['songid']
            pagename=request.form['pagename']
            songimage=request.files['songimage']
            filename = songimage.filename
            extension = os.path.splitext(filename)[1] 
            imgpath='uploads/songs/image/'+ songname + extension
            songimage.save('static/'+imgpath)
            q="update songs set image_loc='%s' where song_id='%s'"%(imgpath,songid)
            update(q)
            flash('success: Image updated successfully')
            if pagename == 'privatesongs':
                return redirect(url_for('uploader.privatesongs'))
            elif pagename == 'pendingsongs':
                return redirect(url_for('uploader.pendingsongs'))
            elif pagename == 'approvedsongs':
                return redirect(url_for('uploader.approvedsongs'))
            elif pagename == 'allsongs':
                return redirect(url_for('uploader.allsongs'))
        if 'songupdate' in request.form:
            songname=request.form['songname']
            songid=request.form['songid']
            album=request.form['album']
            privacy=request.form['privacy']
            genre=request.form['genre']
            date=request.form['date']
            language=request.form['language']
            pagename=request.form['pagename']
            artist_ids = request.form.getlist('artist')
            q="update songs set album_id='%s', song_name='%s', genre='%s', date='%s',language='%s', privacy='%s' where song_id='%s'"%(album,songname,genre,date,language,privacy,songid)
            update(q)
            q="delete from songartist where song_id='%s'"%(songid)
            delete(q)
            for artist_id in artist_ids:
                q="insert into songartist (song_id,artist_id) values('%s','%s')"%(songid,artist_id)
                insert(q)
            flash('success: Song Details updated successfully')
            if pagename == 'privatesongs':
                return redirect(url_for('uploader.privatesongs'))
            elif pagename == 'pendingsongs':
                return redirect(url_for('uploader.pendingsongs'))
            elif pagename == 'approvedsongs':
                return redirect(url_for('uploader.approvedsongs'))
            elif pagename == 'allsongs':
                return redirect(url_for('uploader.allsongs'))
            elif pagename == 'rejectedsongs':
                return redirect(url_for('uploader.rejectedsongs'))
            
        
    return redirect(url_for('uploader.allsongs'))


@uploader.route('/privatesongs' , methods=['GET', 'POST'])
def privatesongs():
    if 'uid' in session:
        login_id = session['login_id']
        uid = session['uid']
        data = {}
        count={}
        login_id = session['login_id']
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        q="SELECT s.song_id, s.song_name, al.album_name, GROUP_CONCAT(ar.artist_name SEPARATOR ', ') AS artist_name, s.date, s.status,s.privacy FROM songs s INNER JOIN songartist sar USING (song_id) INNER JOIN artist ar ON ar.artist_id = sar.artist_id INNER JOIN album al USING (album_id) WHERE s.user_id='%s' and s.privacy='private' GROUP BY s.song_id;"%(uid)
        privatesongdata=select(q)
        data['privatesongdata']=privatesongdata
        q="select * from artist"
        artistdata=select(q)
        data['artistdata'] = artistdata
        q="select * from album"
        albumdata=select(q)
        data['albumdata']=albumdata
        data['currentsongdata']=0
        if request.method == 'POST':
            action = request.form.get('action')
            song_id = action.split('_')[-1]
            q="SELECT s.song_id,s.song_name,al.album_id,al.album_name,GROUP_CONCAT(ar.artist_name SEPARATOR ', ') AS artist_name,s.date,s.image_loc,s.song_loc,s.genre,s.language,s.privacy FROM songs s INNER JOIN songartist sar USING (song_id) INNER JOIN artist ar ON ar.artist_id=sar.artist_id INNER JOIN album al USING (album_id) where s.song_id='%s' GROUP BY s.song_id"%(song_id)
            currentsongdata=select(q)
            data['currentsongdata']=currentsongdata[0]
            q="SELECT artist_id, artist_name FROM artist INNER JOIN songartist USING (artist_id) WHERE song_id='%s'"%(song_id)
            currentartistdata=select(q)
            data['currentartistdata']=currentartistdata
            if action.startswith('update_song'):
                return render_template('uploader/private_songs.html', data=data,count=count, value='updatesong')
            elif action.startswith('view_song'):
                 return render_template('uploader/private_songs.html', data=data,count=count, value='viewsong')
            elif action.startswith('delete_song'):
                # Delete song action
                # Handle the delete song functionality
                return 'Delete Song'
        return render_template('uploader/private_songs.html', data=data,count=count)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))
    
@uploader.route('/analytics' , methods=['GET', 'POST'])
def analytics():
    if 'uid' in session:
        uid = session['uid']
        data = {}
        count={}
        login_id = session['login_id']
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        q="SELECT s.song_id,s.song_name,s.image_loc,COUNT(c.click_id) AS clicks FROM songs s LEFT JOIN clicks c ON s.song_id=c.content_id AND c.content_type='song' WHERE s.user_id='%s' GROUP BY s.song_id"%(uid)
        songdata=select(q)
        data['songdata']=songdata
        q="SELECT DATE(TIMESTAMP) AS dates, COUNT(*) AS clicks FROM clicks c WHERE (content_type = 'song' AND EXISTS (SELECT 1 FROM songs s WHERE s.song_id = c.content_id AND s.user_id = '%s')) OR (content_type = 'album' AND EXISTS (SELECT 1 FROM album a WHERE a.album_id = c.content_id AND a.user_id = '%s')) OR (content_type = 'artist' AND EXISTS (SELECT 1 FROM artist ar WHERE ar.artist_id = c.content_id AND ar.user_id = '%s')) GROUP BY DATE(TIMESTAMP)"%(uid,uid,uid)
        totalclicks=select(q)
        clicks, dates = getClicksDatesInc(totalclicks)
        data['chartdata']={'clicks':clicks,'dates':dates}
        q="SELECT 'Songs' AS name,COUNT(c.content_type) AS clicks FROM clicks c INNER JOIN songs s ON c.content_id=s.song_id AND c.content_type='song' AND s.user_id='%s' GROUP BY name UNION SELECT 'Albums' AS name,COUNT(c.content_type) AS clicks FROM clicks c INNER JOIN album a ON c.content_id=a.album_id AND c.content_type='album' AND a.user_id='%s' GROUP BY name UNION SELECT 'Artists' AS name,COUNT(c.content_type) AS clicks FROM clicks c INNER JOIN artist a ON c.content_id=a.artist_id AND c.content_type='artist' AND a.user_id='%s' GROUP BY name"%(uid,uid,uid)
        clickdata=select(q)
        q = "SELECT al.album_id,al.album_name,al.image_loc,COUNT(c.click_id) AS clicks FROM album al LEFT JOIN clicks c ON al.album_id=c.content_id AND c.content_type='album' WHERE al.user_id='%s' GROUP BY al.album_id"%(uid)
        myalbumdetails=select(q)
        data['myalbumdetails']=myalbumdetails
        q = "SELECT ar.artist_id,ar.artist_name,ar.image_loc,COUNT(c.click_id) AS clicks FROM artist ar LEFT JOIN clicks c ON ar.artist_id=c.content_id AND c.content_type='artist' WHERE ar.user_id='%s' GROUP BY ar.artist_id"%(uid)
        myartistdata=select(q)
        data['myartistdata']=myartistdata
        if 'contenttype' in request.form:
            contenttype = request.form.get('contenttype')
            if contenttype == 'SongClicked':
                song_id = request.form.get('songId')
                q="SELECT DATE(c.timestamp) AS dates,COUNT(*) AS clicks FROM clicks c WHERE c.content_type='song' AND c.content_id='%s' GROUP BY DATE(c.timestamp);"%(song_id)
                songclickdata=select(q)
                clicks, dates = getClicksDatesInc(songclickdata)
                q="select * from songs where song_id='%s'"%(song_id)
                songdata=select(q)
                return jsonify({'clicks': clicks, 'dates': dates,'songdata':songdata[0]})
        return render_template('uploader/analytics.html', data=data,count=count,clickdata=clickdata)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@uploader.route('/analytics_overview' , methods=['GET', 'POST'])
def analytics_overview():
    if 'uid' in session:
        uid = session['uid']
        data = {}
        count={}
        login_id = session['login_id']
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        if request.method == 'POST':
            song_id = request.form.get('songId')
            album_id = request.form.get('albumId')
            artist_id = request.form.get('artistId')
            if song_id:
                q="SELECT DATE(c.timestamp) AS dates,COUNT(*) AS clicks FROM clicks c WHERE c.content_type='song' AND c.content_id='%s' GROUP BY DATE(c.timestamp);"%(song_id)
                songclickdata=select(q)
                q="select * from songs where song_id='%s'"%(song_id)
                songdata=select(q)
                data['contentdata']=songdata[0] #Song data
                q="SELECT DATE(l.timestamp) AS dates,COUNT(*) AS likes FROM likes l WHERE l.content_type='song' AND l.content_id='%s' GROUP BY DATE(l.timestamp)"%(song_id)
                songlikes=select(q)
                clicks, likes, dates = getClicksLikesDates(songclickdata, songlikes)
                data['chartdata']={'clicks':clicks,'dates':dates,'likes':likes}
                return render_template('uploader/analytics_overview.html', data=data, count=count)
            elif album_id:
                q="SELECT DATE(c.timestamp) AS dates,COUNT(*) AS clicks FROM clicks c WHERE c.content_type='album' AND c.content_id='%s' GROUP BY DATE(c.timestamp);"%(album_id)
                albumclickdata=select(q)
                q="select * from album where album_id='%s'"%(album_id)
                albumdata=select(q)
                data['contentdata']=albumdata[0] #Album data
                q="SELECT DATE(l.timestamp) AS dates,COUNT(*) AS likes FROM likes l WHERE l.content_type='album' AND l.content_id='%s' GROUP BY DATE(l.timestamp)"%(album_id)
                albumlikes=select(q)
                clicks, likes, dates = getClicksLikesDates(albumclickdata, albumlikes)
                data['chartdata']={'clicks':clicks,'dates':dates,'likes':likes}
                return render_template('uploader/analytics_overview.html', data=data, count=count)
            elif artist_id:
                q="SELECT DATE(c.timestamp) AS dates,COUNT(*) AS clicks FROM clicks c WHERE c.content_type='artist' AND c.content_id='%s' GROUP BY DATE(c.timestamp);"%(artist_id)
                artistclickdata=select(q)
                q="select * from artist where artist_id='%s'"%(artist_id)
                artistdata=select(q)
                data['contentdata']=artistdata[0] #Artist data
                q="SELECT DATE(l.timestamp) AS dates,COUNT(*) AS likes FROM likes l WHERE l.content_type='artist' AND l.content_id='%s' GROUP BY DATE(l.timestamp)"%(artist_id)
                artistlikes=select(q)
                clicks, likes, dates = getClicksLikesDates(artistclickdata, artistlikes)
                data['chartdata']={'clicks':clicks,'dates':dates,'likes':likes}
                return render_template('uploader/analytics_overview.html', data=data, count=count)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))
    

@uploader.route('/profile')
def profile():
    if 'uid' in session:
        login_id = session['login_id']
        uid = session['uid']
        data = {}
        count={}
        login_id = session['login_id']
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT u.user_id,u.login_id,u.fname,u.lname,u.email,u.mobile,u.image_loc,u.status,l.username,l.password FROM USER u INNER JOIN login l ON u.login_id=l.login_id WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        return render_template('uploader/uploader_profile.html', data=data,count=count)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))
    

@uploader.route('/artist', methods=['GET', 'POST'])
def artist():
    if 'uid' in session:
        login_id = session['login_id']
        uid = session['uid']
        data = {}
        count={}
        login_id = session['login_id']
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        q = "SELECT ar.artist_id, ar.artist_name, ar.image_loc, ar.cover_pic, COUNT(s.song_id) AS song_count FROM artist ar LEFT JOIN songartist sar ON ar.artist_id = sar.artist_id LEFT JOIN songs s ON s.song_id = sar.song_id AND s.privacy = 'public' AND s.status = 'approved' GROUP BY ar.artist_id ORDER BY ar.artist_id"
        artistdata=select(q)
        data['userdetails'] = res[0]
        data['artistdetails']=artistdata
        data['currentartistsongs']=''
        data['currentartistdetails']=''
        if request.method == 'POST':
            if 'addartistbtn' in request.form:
                artistname = request.form['artistname']
                artist_image = request.files['image']
                cover_image = request.files['coverimage']
                q="insert into artist (artist_name,image_loc,cover_pic,user_id) values ('%s','null','null','%s')"%(artistname,uid)
                id=insert(q)
                updateArtistImage(artist_image,id)
                updateArtistCover(cover_image,id)
                if q :
                    flash('success: Artist added successfully')
                    return redirect(url_for('uploader.artist'))
                else:
                    flash('danger: Artist not added')
                    return redirect(url_for('uploader.artist'))
            elif 'viewartistaction' in request.form:
                viewartistaction = request.form.get('viewartistaction')
                artist_id = viewartistaction.split('_')[-1]
                q="SELECT * FROM artist WHERE artist_id='%s'"%(artist_id)
                currentartistdetails=select(q)
                data['currentartistdetails']=currentartistdetails[0]
                q="SELECT s.song_id, s.song_name, IFNULL(al.album_name, 'No album') AS album_name, s.image_loc, s.song_loc, s.genre, s.date, s.language, s.duration FROM songs s LEFT JOIN album al ON s.album_id = al.album_id AND s.status = 'approved' AND s.privacy = 'public' INNER JOIN songartist sa ON sa.song_id = s.song_id AND sa.artist_id = '%s'"%(artist_id)
                currentartistsongs=select(q)
                data['currentartistsongs']=currentartistsongs
                return render_template('uploader/artist.html', data=data,count=count,value='viewartist')
        return render_template('uploader/artist.html', data=data,count=count)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))
    
@uploader.route('/myartist', methods=['GET', 'POST'])
def myartist():
    if 'uid' in session:
        login_id = session['login_id']
        uid = session['uid']
        data = {}
        count={}
        login_id = session['login_id']
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        q = "SELECT ar.artist_id, ar.artist_name, ar.image_loc, ar.cover_pic, COUNT(s.song_id) AS song_count FROM artist ar LEFT JOIN songartist sar ON ar.artist_id = sar.artist_id LEFT JOIN songs s ON s.song_id = sar.song_id AND s.privacy = 'public' AND s.status = 'approved' WHERE ar.user_id='%s' GROUP BY ar.artist_id ORDER BY ar.artist_id"%(uid)
        artistdata=select(q)
        data['userdetails'] = res[0]
        data['artistdetails']=artistdata
        data['currentartistsongs']=''
        data['currentartistdetails']=''
        if request.method == 'POST':
            if 'addartistbtn' in request.form:
                artistname = request.form['artistname']
                artist_image = request.files['image']
                cover_image = request.files['coverimage']
                q="insert into artist (artist_name,image_loc,cover_pic,user_id) values ('%s','null','null','%s')"%(artistname,uid)
                id=insert(q)
                updateArtistImage(artist_image,id)
                updateArtistCover(cover_image,id)
                if q :
                    flash('success: Artist added successfully')
                    return redirect(url_for('uploader.myartist'))
                else:
                    flash('danger: Artist not added')
                    return redirect(url_for('uploader.myartist'))
            elif 'artistaction' in request.form:
                artistaction = request.form.get('artistaction')
                artist_id = artistaction.split('_')[-1]
                q="SELECT * FROM artist WHERE artist_id='%s'"%(artist_id)
                currentartistdetails=select(q)
                data['currentartistdetails']=currentartistdetails[0]
                if artistaction.startswith('view_artist'):
                    q="SELECT s.song_id, s.song_name, IFNULL(al.album_name, 'No album') AS album_name, s.image_loc, s.song_loc, s.genre, s.date, s.language, s.duration FROM songs s LEFT JOIN album al ON s.album_id = al.album_id AND s.status = 'approved' AND s.privacy = 'public' INNER JOIN songartist sa ON sa.song_id = s.song_id AND sa.artist_id = '%s'"%(artist_id)
                    currentartistsongs=select(q)
                    data['currentartistsongs']=currentartistsongs
                    return render_template('uploader/myartist.html', data=data,count=count,value='viewartist')
                elif artistaction.startswith('update_artist'):
                    return render_template('uploader/myartist.html', data=data,count=count,value='editartist')
                elif artistaction.startswith('delete_artist'):
                    message=deleteArtist(artist_id)
                    flash(message)
                    return redirect(url_for('uploader.myartist'))
            elif 'submitArtistImage' in request.form:
                artist_image = request.files['artistImage']
                if artist_image.filename !='':
                    artistid = request.form['artistid']
                    updateArtistImage(artist_image,artistid)
                    flash("success: Updated Artist Image successfully")
                    return redirect(url_for('uploader.myartist'))
                else:
                    flash("danger: Add Artist image first")
            elif 'submitCoverImage' in request.form:
                cover_image = request.files['coverImage']
                if cover_image.filename !='':
                    artistid = request.form['artistid']
                    updateArtistCover(cover_image,artistid)
                    flash("success: Updated Artist Cover successfully")
                    return redirect(url_for('uploader.myartist'))
                else:
                    flash("danger: Add Cover image first")
            elif 'nameupdate' in request.form:
                artistid = request.form['artistid']
                artistname = request.form['artist_name']
                q="update artist set artist_name='%s' where artist_id='%s'"%(artistname,artistid)
                update(q)
                flash("success: Updated Artist Name")
                return redirect(url_for('uploader.myartist'))
            elif 'songaction' in request.form:
                songaction = request.form.get('songaction')
                song_id = songaction.split('_')[-1]
                q="SELECT u.login_id FROM USER u INNER JOIN songs s ON s.user_id=u.user_id WHERE song_id='%s'"%(song_id)
                login_id=select(q)
                login_id=login_id[0]['login_id']
                q="insert into notification(user_id,content_id,content,content_status,status,notification_type) values('%s','%s','Song removed from artist','artistremoved','toread','songremoval')"%(login_id,song_id)
                insert(q)
                q="DELETE from songartist where song_id='%s'"%(song_id)
                delete(q)

                flash("warning: Song removed"+song_id)
                return redirect(url_for('uploader.myartist'))
                
        return render_template('uploader/myartist.html', data=data,count=count)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))
    

@uploader.route('/album', methods=['GET', 'POST'])
def album():
    if 'uid' in session:
        login_id = session['login_id']
        uid = session['uid']
        data = {}
        count={}
        login_id = session['login_id']
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        q = "SELECT al.album_id, al.album_name, al.image_loc, al.cover_pic, COUNT(s.song_id) AS song_count FROM album al LEFT JOIN songs s ON al.album_id = s.album_id AND s.privacy = 'public' AND s.status = 'approved' GROUP BY al.album_id, al.album_name, al.image_loc, al.cover_pic ORDER BY al.album_id"
        albumdata=select(q)
        data['userdetails'] = res[0]
        data['albumdetails']=albumdata
        data['currentalbumdetails']=''
        data['albumsongdata']=''
        if request.method == 'POST':
            if 'uploadalbum' in request.form:
                albumname = request.form['albumname']
                album_image = request.files['image']
                cover_image = request.files['coverimage']
                q="insert into album (album_name,image_loc,cover_pic,user_id) values ('%s','null','null','%s')"%(albumname,uid)
                id=insert(q)
                updateAlbumCover(cover_image,id)
                updateAlbumImage(album_image,id)
                if q :
                    flash('success: Album added successfully')
                    return redirect(url_for('uploader.album'))
                else:
                    flash('danger: Album not added')
                    return redirect(url_for('uploader.album'))
            elif 'action' in request.form:
                action = request.form.get('action')
                album_id = action.split('_')[-1]
                if action.startswith('view_album'):
                    q="select * from album where album_id='%s'"%(album_id)
                    currentalbumdetails=select(q)
                    data['currentalbumdetails']=currentalbumdetails[0]
                    q="SELECT DISTINCT s.song_id, s.song_name, GROUP_CONCAT(ar.artist_name SEPARATOR ', ') AS artist_name, s.song_loc FROM songs s INNER JOIN songartist sar USING (song_id) INNER JOIN artist ar ON ar.artist_id = sar.artist_id WHERE s.privacy='public' AND s.STATUS='approved' AND s.album_id='%s' GROUP BY sar.song_id ORDER BY song_id"%(album_id)
                    albumsongdata=select(q)
                    data['albumsongdata']=albumsongdata
                    return render_template('uploader/album.html', data=data,count=count, value='viewalbum')
        return render_template('uploader/album.html', data=data,count=count)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@uploader.route('/myalbum', methods=['GET', 'POST'])
def myalbum():
    if 'uid' in session:
        login_id = session['login_id']
        uid = session['uid']
        data = {}
        count={}
        login_id = session['login_id']
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        q = "SELECT al.album_id, al.album_name, al.image_loc, al.cover_pic, COUNT(s.song_id) AS song_count FROM album al LEFT JOIN songs s ON al.album_id = s.album_id AND s.privacy = 'public' AND s.status = 'approved' WHERE al.user_id = '%s' GROUP BY al.album_id, al.album_name, al.image_loc, al.cover_pic ORDER BY al.album_id"%(uid)
        myalbumdata=select(q)
        data['userdetails'] = res[0]
        data['myalbumdetails']=myalbumdata
        data['currentalbumdetails']=''
        data['albumsongdata']=''
        if request.method == 'POST':
            if 'uploadalbum' in request.form:
                albumname = request.form['albumname']
                album_image = request.files['image']
                cover_image = request.files['coverimage']
                q="insert into album (album_name,image_loc,cover_pic,user_id) values ('%s','null','null','%s')"%(albumname,uid)
                id=insert(q)
                updateAlbumCover(cover_image,id)
                updateAlbumImage(album_image,id)
                if q :
                    flash('success: Album added successfully')
                    return redirect(url_for('uploader.myalbum'))
                else:
                    flash('danger: Album not added')
                    return redirect(url_for('uploader.myalbum'))
            elif 'action' in request.form:
                action = request.form.get('action')
                album_id = action.split('_')[-1]
                if action.startswith('view_album'):
                    q="select * from album where album_id='%s'"%(album_id)
                    currentalbumdetails=select(q)
                    data['currentalbumdetails']=currentalbumdetails[0]
                    q="SELECT DISTINCT s.song_id, s.song_name, GROUP_CONCAT(ar.artist_name SEPARATOR ', ') AS artist_name, s.song_loc FROM songs s INNER JOIN songartist sar USING (song_id) INNER JOIN artist ar ON ar.artist_id = sar.artist_id WHERE s.privacy='public' AND s.STATUS='approved' AND s.album_id='%s' GROUP BY sar.song_id ORDER BY song_id"%(album_id)
                    albumsongdata=select(q)
                    data['albumsongdata']=albumsongdata
                    return render_template('uploader/myalbum.html', data=data,count=count, value='viewalbum')
                elif action.startswith('update_album'):
                    q="select * from album where album_id='%s'"%(album_id)
                    currentalbumdetails=select(q)
                    data['currentalbumdetails']=currentalbumdetails[0]
                    return render_template('uploader/myalbum.html', data=data,count=count, value='editalbum')
                elif action.startswith('delete_album'):
                    message=deleteAlbum(album_id)
                    flash(message)
                    return redirect(url_for('uploader.myalbum'))
            elif 'submitAlbumImage' in request.form:
                album_image = request.files['albumImage']
                if album_image.filename !='':
                    albumid = request.form['albumid']
                    albumname = request.form['albumname']
                    updateAlbumImage(album_image,albumid)
                    flash("success: Updated Album Image successfully")
                    return redirect(url_for('uploader.myalbum'))
                else:
                    flash("danger: Add Album image first")
            elif 'submitCoverImage' in request.form:
                cover_image = request.files['coverImage']
                if cover_image.filename !='':
                    albumid = request.form['albumid']
                    albumname = request.form['albumname']
                    updateAlbumCover(cover_image,albumid)
                    flash("success: Updated Album Cover successfully")
                    return redirect(url_for('uploader.myalbum'))
                else:
                    flash("danger: Add Cover image first")
            elif 'nameupdate' in request.form:
                albumid = request.form['albumid']
                albumname = request.form['album_name']
                q="update album set album_name='%s' where album_id='%s'"%(albumname,albumid)
                update(q)
                flash("success: Updated Album Name")
                return redirect(url_for('uploader.myalbum'))
            elif 'songaction' in request.form:
                songaction = request.form.get('songaction')
                song_id = songaction.split('_')[-1]
                q="SELECT u.login_id FROM USER u INNER JOIN songs s ON s.user_id=u.user_id WHERE song_id='%s'"%(song_id)
                login_id=select(q)
                login_id=login_id[0]['login_id']
                q="insert into notification(user_id,content_id,content,content_status,status,notification_type) values('%s','%s','Song removed from album','albumremoved','toread','songremoval')"%(login_id,song_id)
                insert(q)
                q="update songs set album_id='0' where song_id='%s'"%(song_id)
                update(q)
                flash("warning: Song removed")
                return redirect(url_for('uploader.myalbum'))
        return render_template('uploader/myalbum.html', data=data,count=count)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

    
@uploader.route('/uploadmusic', methods=['GET', 'POST'])
def uploadmusic():
        if 'uid' in session:
            login_id = session['login_id']
            uid = session['uid']
            data = {}
            count={}
            login_id = session['login_id']
            q="SELECT n.notification_type,s.song_name,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND content_status='approved' AND notification_type='approvals' AND n.user_id='%s'"%(login_id)
            approvednotificationdata=select(q)
            data['approvednotificationdata']=approvednotificationdata
            count['notification']=str(len(data['approvednotificationdata']))
            q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
            res = select(q)
            data['userdetails'] = res[0]
            if request.method == 'POST':
                file = request.files['file']
                if file and file.filename.endswith('.mp3'):
                    audio_file = file
                    prediction = genrePrediction(audio_file)
                    audio = MP3(file)
                    duration_in_seconds = str(int(audio.info.length))
                    file_extension = os.path.splitext(file.filename)[1]
                    songpath='uploads/songs/' +res[0]['fname']+str(uuid.uuid4()) + file_extension
                    file.save('static/'+songpath)
                    songpathdb='/static/'+songpath # To store in database with /static as it may sometimes conflict with the save if given in .save
                    session['songpath']=songpathdb
                    session['predictedgenre']=prediction
                    duration_in_min=secondstominute(int(duration_in_seconds))
                    session['songduration']=duration_in_min
                    flash("success: saved the song.")
                    flash("info: Predicted Genre is "+prediction)
                    return redirect(url_for('uploader.uploadsong'))
                else:
                    flash("Invalid file format. Please upload an MP3 file.")
                    return render_template('uploader/home.html', data=data,count=count)
            return render_template('uploader/home.html', data=data,count=count)
        

@uploader.route('/uploadsong', methods=['GET', 'POST'])
def uploadsong():
    if 'uid' in session:
        login_id = session['login_id']
        uid = session['uid']
        data = {}
        count={}
        pgenre=session['predictedgenre']
        data['predictedgenre']=pgenre
        login_id = session['login_id']
        q="SELECT n.notification_type,s.song_name,n.content_status,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND n.user_id='%s'"%(login_id)
        notificationdata=select(q)
        data['notificationdata']=notificationdata
        count['notification']=str(len(data['notificationdata']))
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]        #A flash message is there for upload successfull in return render_template('uploader/home.html', data=data,count=count)
        q="select * from artist"
        artistdata=select(q)
        data['artistdata'] = artistdata
        q="select * from album"
        albumdata=select(q)
        data['albumdata']=albumdata
        if 'SongUploadBtn' in request.form:
            songname=request.form['songname']
            image = request.files['image']
            album=request.form['album']
            artist_ids = request.form.getlist('artist') 
            genre=request.form['genre']
            date=request.form['date']
            language=request.form['language']
            privacy=request.form['privacy']
            songpath=session['songpath']
            songduration=session['songduration']
            
            # Get the file extensions
            song_image_extension = os.path.splitext(image.filename)[1]

            # Specify the path where you want to save the uploaded files
            upload_folder = 'static/uploads/songs/image'  # Update the path according to your setup

            # Create the upload folder if it doesn't exist
            os.makedirs(upload_folder, exist_ok=True)

            # Customize the filenames
            song_image_filename = songname + song_image_extension

            # Saving the path for database
            songimagepath='uploads/songs/image/' + songname + song_image_extension

            # Save the uploaded files with the customized filenames
            image.save(os.path.join(upload_folder, song_image_filename))

            # Save to database 
            q="insert into songs (album_id,song_name,image_loc,song_loc,genre,date,language,user_id,privacy,duration,status) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(album,songname,songimagepath,songpath,genre,date,language,uid,privacy,songduration,'pending')
            ins=insert(q)
            if ins:
                flash('success: Song uploaded successfully')
                q="insert into notification(user_id,content_id,content,content_status,status,notification_type) values('1','%s','Song pending for approval','pending','toread','approvals')"%(ins)
                nid=insert(q)
                for artist_id in artist_ids:
                    q="insert into songartist (song_id,artist_id) values ('%s','%s')"%(ins,artist_id)
                    SAid=insert(q)
                if privacy == 'public':
                    return redirect(url_for('uploader.pendingsongs'))
                else:
                    return redirect(url_for('uploader.privatesongs'))
        if 'SongCancelBtn' in request.form:
            songpath=session['songpath']
            songpath=songpath[1:]
            if os.path.exists(songpath):
                os.remove(songpath)
            return redirect(url_for('uploader.home'))
        return render_template('uploader/uploadsong.html', data=data,count=count)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))
    
@uploader.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    if 'uid' in session:
        login_id = session['login_id']
        uid = session['uid']
        current_pass = request.form['password']
        new_pass = request.form['newpassword']
        renew_pass = request.form['renewpassword']
        q="select * from login where login_id='%s'"%(login_id)
        logindetails=select(q)
        if len(logindetails) > 0 :
            if logindetails[0]['password'] == current_pass:
                if new_pass == renew_pass:
                    q="update login set password='%s' where login_id='%s'"%(new_pass,login_id)
                    update(q)
                    flash("success: Password Changed successfully")
                else:
                    flash("danger: New password and Re entered password does not match")
            else:
                flash("danger: Current password does not match")
        else:
            flash("danger: Error changing the password")
        return redirect(url_for('uploader.profile'))
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@uploader.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'uid' in session:
        login_id = session['login_id']
        uid = session['uid']
        fname = request.form['fName']
        lname = request.form['lName']
        mob = request.form['phone']
        email = request.form['email']
        image = request.files['profileImage']
        print('File name of image :',image.filename)
        q="update user set fname='%s', lname='%s', email='%s', mobile='%s' where user_id='%s'"%(fname,lname,email,mob,uid)
        update(q)
        if image.filename != '':
            UpdateProfileImage(image,uid)
        flash("success: Profile successfully updated")
        return redirect(url_for('uploader.profile'))
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))
    
@uploader.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('public.home'))

def secondstominute(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60

    if minutes == 0:
        return f"0:{remaining_seconds:02d}"
    else:
        return f"{minutes}:{remaining_seconds:02d}"
    
def genrePrediction(audio_file):
    # random string of digits for file name
    file_name = str(random.randint(0, 100000))

    # save the file locally
    audio_file.save(file_name)

    # check the file extension
    file_extension = audio_file.filename.split(".")[-1]

    if file_extension == "mp3":
        # convert MP3 to WAV
        wav_file_name = file_name + ".wav"
        audio = AudioSegment.from_mp3(file_name)
        audio.export(wav_file_name, format="wav")
        audio_file = wav_file_name

    # invoke the genre recognition service
    grs = Genre_Recognition_Service()

    # make prediction
    prediction = grs.predict(file_name)

    # remove the temporary file
    os.remove(file_name)
    if file_extension == "mp3":
        os.remove(wav_file_name)

    return prediction
