from flask import *
from database import*
from deletion import *

admin =Blueprint('admin',__name__)

@admin.route('/admin_home')
def admin_home():
    if 'login_id' in session:
        login_id = session['login_id']
        data={}
        count={}
        q="SELECT n.notification_type,s.song_name,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND content_status='pending' AND notification_type='approvals' AND n.user_id='1'"
        approvalnotificationdata=select(q)
        data['approvalnotificationdata']=approvalnotificationdata
        count['notification']=str(len(data['approvalnotificationdata']))
        q="select count(*) as song_count from songs where privacy = 'public'"
        song_count=select(q)
        count['song_count']=song_count[0]['song_count']
        q="select count(*) as album_count from album"
        album_count=select(q)
        count['album_count']=album_count[0]['album_count']
        q="select count(*) as active_users_count from user where status='active'"
        active_users_count=select(q)
        count['active_users_count']=active_users_count[0]['active_users_count']
        
        return render_template('admin/index.html', data=data,count=count)
    else:
        return redirect(url_for('public.home'))

@admin.route('/approvals' , methods=['GET', 'POST'])
def approvals():
    if 'login_id' in session:
        login_id = session['login_id']
        data = {}
        count={}
        q="update notification set status='read' where notification_type='approvals' and user_id='%s'"%(login_id)
        update(q) # updates the notification table as read for approval notifications
        q="SELECT n.notification_type,s.song_name,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND content_status='pending' AND notification_type='approvals' AND n.user_id='1'"
        approvalnotificationdata=select(q)
        data['approvalnotificationdata']=approvalnotificationdata
        count['notification']=str(len(data['approvalnotificationdata']))
        q="SELECT s.song_id, s.song_name, al.album_name, GROUP_CONCAT(ar.artist_name SEPARATOR ', ') AS artist_name, s.date, s.status,s.privacy FROM songs s INNER JOIN songartist sar USING (song_id) INNER JOIN artist ar ON ar.artist_id = sar.artist_id INNER JOIN album al USING (album_id) WHERE s.privacy='public' AND s.STATUS='pending' GROUP BY s.song_id ORDER BY song_id DESC"
        pendingsongdata=select(q)
        data['pendingsongdata'] = pendingsongdata
        data['currentsongdata']={}
        if request.method == 'POST':
            action = request.form.get('action')
            song_id = action.split('_')[-1]
            if action.startswith('approve_song'):
                q="update songs set status='approved' where song_id='%s'"%(song_id)
                update(q)
                q="SELECT login_id FROM USER INNER JOIN songs USING (user_id) WHERE song_id='%s'"%(song_id)
                songuserdata=select(q)
                print("Notification user id:",songuserdata)
                user_id=songuserdata[0]['login_id']
                q="insert into notification(user_id,content_id,content,content_status,status,notification_type) values('%s','%s','Song Approved','approved','toread','approvals')"%(user_id,song_id)
                nid=insert(q)
                flash("success: Song Approved Successfully"+song_id)
                return redirect(url_for('admin.approvals'))
            elif action.startswith('view_song'):
                 q="SELECT s.song_id,s.song_name,al.album_id,al.album_name,GROUP_CONCAT(ar.artist_name SEPARATOR ', ') AS artist_name,s.date,s.image_loc,s.song_loc,s.genre,s.language,s.privacy FROM songs s INNER JOIN songartist sar USING (song_id) INNER JOIN artist ar ON ar.artist_id=sar.artist_id INNER JOIN album al USING (album_id) where s.song_id='%s' GROUP BY s.song_id"%(song_id)
                 currentsongdata=select(q)
                 data['currentsongdata']=currentsongdata[0]
                 return render_template('admin/approvals.html', data=data, value='viewsong',count=count)
            elif action.startswith('reject_song'):
                q="update songs set status='rejected' where song_id='%s'"%(song_id)
                update(q)
                flash("warning: Song Rejected Successfully")
                return redirect(url_for('admin.approvals'))
        return render_template('admin/approvals.html',data=data,count=count)
    else:
        return redirect(url_for('public.home'))
    
@admin.route('/allsongs' , methods=['GET', 'POST'])
def allsongs():
    if 'login_id' in session:
        login_id = session['login_id']
        data = {}
        count={}
        q="SELECT n.notification_type,s.song_name,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND content_status='pending' AND notification_type='approvals' AND n.user_id='1'"
        approvalnotificationdata=select(q)
        data['approvalnotificationdata']=approvalnotificationdata
        count['notification']=str(len(data['approvalnotificationdata']))
        q="SELECT s.song_id, s.song_name, al.album_name, GROUP_CONCAT(ar.artist_name SEPARATOR ', ') AS artist_name, s.date, s.status,s.privacy FROM songs s INNER JOIN songartist sar USING (song_id) INNER JOIN artist ar ON ar.artist_id = sar.artist_id INNER JOIN album al USING (album_id) WHERE s.privacy='public' GROUP BY s.song_id ORDER BY song_id DESC"
        allsongdata=select(q)
        data['allsongdata'] = allsongdata
        data['currentsongdata']={}
        if request.method == 'POST':
            action = request.form.get('action')
            song_id = action.split('_')[-1]
            if action.startswith('approve_song'):
                q="update songs set status='approved' where song_id='%s'"%(song_id)
                update(q)
                q="SELECT login_id FROM USER INNER JOIN songs USING (user_id) WHERE song_id='%s'"%(song_id)
                songuserdata=select(q)
                user_id=songuserdata[0]['login_id']
                q="insert into notification(user_id,content_id,content,content_status,status,notification_type) values('%s','%s','Song Approved','approved','toread','approvals')"%(user_id,song_id)
                nid=insert(q)
                flash("success: Song Approved Successfully"+song_id)
                return redirect(url_for('admin.allsongs'))
            elif action.startswith('view_song'):
                 q="SELECT s.song_id,s.song_name,al.album_id,al.album_name,GROUP_CONCAT(ar.artist_name SEPARATOR ', ') AS artist_name,s.date,s.image_loc,s.song_loc,s.genre,s.language,s.privacy FROM songs s INNER JOIN songartist sar USING (song_id) INNER JOIN artist ar ON ar.artist_id=sar.artist_id INNER JOIN album al USING (album_id) where s.song_id='%s' GROUP BY s.song_id"%(song_id)
                 currentsongdata=select(q)
                 data['currentsongdata']=currentsongdata[0]
                 return render_template('admin/allsongs.html', data=data, value='viewsong',count=count)
            elif action.startswith('delete_song'):
                message = songDeletion(song_id)
                flash(message)
                return redirect(url_for('admin.allsongs'))
            elif action.startswith('reject_song'):
                q="update songs set status='rejected' where song_id='%s'"%(song_id)
                update(q)
                flash("warning: Song Rejected Successfully")
                return redirect(url_for('admin.allsongs'))
        return render_template('admin/allsongs.html',data=data,count=count)
    else:
        return redirect(url_for('public.home'))
    
@admin.route('/artist', methods=['GET', 'POST'])
def artist():
    if 'login_id' in session:
        login_id = session['login_id']
        data = {}
        count={}
        q="SELECT n.notification_type,s.song_name,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND content_status='pending' AND notification_type='approvals' AND n.user_id='1'"
        approvalnotificationdata=select(q)
        data['approvalnotificationdata']=approvalnotificationdata
        count['notification']=str(len(data['approvalnotificationdata']))
        q = "SELECT ar.artist_id, ar.artist_name, ar.image_loc, ar.cover_pic, COUNT(s.song_id) AS song_count FROM artist ar LEFT JOIN songartist sar ON ar.artist_id = sar.artist_id LEFT JOIN songs s ON s.song_id = sar.song_id AND s.privacy = 'public' AND s.status = 'approved' GROUP BY ar.artist_id ORDER BY ar.artist_id"
        artistdata=select(q)
        data['artistdetails'] = artistdata
        data['currentartistdetails']={}
        if request.method == 'POST':
            action = request.form.get('action')
            artist_id = action.split('_')[-1]
            if action.startswith('view_artist'):
                 q="SELECT * FROM artist WHERE artist_id='%s'"%(artist_id)
                 currentartistdetails=select(q)
                 data['currentartistdetails']=currentartistdetails[0]
                 q="SELECT s.song_id, s.song_name, IFNULL(al.album_name, 'No album') AS album_name, s.image_loc, s.song_loc, s.genre, s.date, s.language, s.duration FROM songs s LEFT JOIN album al ON s.album_id = al.album_id AND s.status = 'approved' AND s.privacy = 'public' INNER JOIN songartist sa ON sa.song_id = s.song_id AND sa.artist_id = '%s'"%(artist_id)
                 currentartistsongs=select(q)
                 data['currentartistsongs']=currentartistsongs
                 return render_template('admin/artist.html', data=data, value='viewartist',count=count)
            elif action.startswith('delete_artist'):
                message = deleteArtist(artist_id)
                flash(message)
                return redirect(url_for('admin.artist'))
        return render_template('admin/artist.html',data=data,count=count)
    else:
        return redirect(url_for('public.home'))

@admin.route('/album', methods=['GET', 'POST'])
def album():
     if 'login_id' in session:
        login_id = session['login_id']
        data = {}
        count={}
        q="SELECT n.notification_type,s.song_name,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND content_status='pending' AND notification_type='approvals' AND n.user_id='1'"
        approvalnotificationdata=select(q)
        data['approvalnotificationdata']=approvalnotificationdata
        count['notification']=str(len(data['approvalnotificationdata']))
        q="SELECT al.album_id, al.album_name, al.image_loc, al.cover_pic, COUNT(s.song_id) AS song_count FROM album al LEFT JOIN songs s ON al.album_id = s.album_id AND s.privacy = 'public' AND s.status = 'approved' GROUP BY al.album_id, al.album_name, al.image_loc, al.cover_pic ORDER BY al.album_id"
        albumdetails=select(q)
        data['albumdetails'] = albumdetails
        data['currentalbumdetails']={}
        if request.method == 'POST':
            action = request.form.get('action')
            album_id = action.split('_')[-1]
            if action.startswith('view_album'):
                 q="select * from album where album_id='%s'"%(album_id)
                 currentalbumdetails=select(q)
                 data['currentalbumdetails']=currentalbumdetails[0]
                 q="SELECT DISTINCT s.song_id, s.song_name, GROUP_CONCAT(ar.artist_name SEPARATOR ', ') AS artist_name, s.song_loc FROM songs s INNER JOIN songartist sar USING (song_id) INNER JOIN artist ar ON ar.artist_id = sar.artist_id WHERE s.privacy='public' AND s.STATUS='approved' AND s.album_id='%s' GROUP BY sar.song_id ORDER BY song_id"%(album_id)
                 albumsongdata=select(q)
                 data['albumsongdata']=albumsongdata
                 return render_template('admin/album.html', data=data, value='viewalbum',count=count)
            elif action.startswith('delete_album'):
                message = deleteAlbum(album_id)
                flash(message)
                return redirect(url_for('admin.album'))
        return render_template('admin/album.html',data=data,count=count)
     else:
        return redirect(url_for('public.home'))
     
@admin.route('/allusers', methods=['GET', 'POST'])
def allusers():
    if 'login_id' in session:
        login_id = session['login_id']
        data = {}
        count={}
        q="SELECT n.notification_type,s.song_name,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND content_status='pending' AND notification_type='approvals' AND n.user_id='1'"
        approvalnotificationdata=select(q)
        data['approvalnotificationdata']=approvalnotificationdata
        count['notification']=str(len(data['approvalnotificationdata']))
        q="select * from user"
        alluserdetails=select(q)
        data['alluserdetails']=alluserdetails
        if request.method == 'POST':
            action = request.form.get('action')
            user_id = action.split('_')[-1]
            if action.startswith('view_user'):
                 q="select * from user where user_id='%s'"%(user_id)
                 currentuserdetails=select(q)
                 data['currentuserdetails']=currentuserdetails[0]
                 return render_template('admin/allusers.html', data=data, value='viewuser',count=count)
            elif action.startswith('deactivate_user'):
                # message = deleteAlbum(album_id)
                # flash(message)
                return redirect(url_for('admin.allusers'))
            elif action.startswith('activate_user'):
                # message = deleteAlbum(album_id)
                # flash(message)
                return redirect(url_for('admin.allusers'))
        return render_template('admin/allusers.html',data=data,count=count)
    else:
        return redirect(url_for('public.home'))

@admin.route('/active_users', methods=['GET', 'POST'])
def active_users():
    if 'login_id' in session:
        login_id = session['login_id']
        data = {}
        count={}
        q="SELECT n.notification_type,s.song_name,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND content_status='pending' AND notification_type='approvals' AND n.user_id='1'"
        approvalnotificationdata=select(q)
        data['approvalnotificationdata']=approvalnotificationdata
        count['notification']=str(len(data['approvalnotificationdata']))

        return render_template('admin/active_users.html',data=data,count=count)
    else:
        return redirect(url_for('public.home'))

@admin.route('/deactive_users', methods=['GET', 'POST'])
def deactive_users():
    if 'login_id' in session:
        login_id = session['login_id']
        data = {}
        count={}
        q="SELECT n.notification_type,s.song_name,n.timestamp FROM notification n INNER JOIN songs s ON s.song_id=n.content_id WHERE n.status='toread' AND content_status='pending' AND notification_type='approvals' AND n.user_id='1'"
        approvalnotificationdata=select(q)
        data['approvalnotificationdata']=approvalnotificationdata
        count['notification']=str(len(data['approvalnotificationdata']))

        return render_template('admin/deactive_users.html',data=data,count=count)
    else:
        return redirect(url_for('public.home'))

@admin.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('public.home'))