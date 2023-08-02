from flask import *
from database import *
import os
from trending import *
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from categories import *
from other_processing import *
from deletion import *
from other_functions import *
user = Blueprint('user',__name__)

@user.route('/user_home')
def user_home():
    if 'uid' in session:
        uid=session['uid']
        data={}
        q="select * from user where user_id='%s'"%(uid)
        res=select(q)
        data['userdetails']=res[0]
        albumdata = get_album_data() #Trending Albums Top 5
        data['albumdata']=albumdata
        artistdata=get_artist_data() #Trending Artists Top 5
        data['artistdata']=artistdata
        q="SELECT s.song_id, s.song_name, al.album_name, s.image_loc AS song_image_loc, s.song_loc, s.genre, s.language, s.duration, CASE WHEN l.content_id IS NOT NULL THEN 'yes' ELSE 'no' END AS liked FROM songs s INNER JOIN likes l ON s.song_id = l.content_id AND l.content_type = 'song' AND l.user_id = '%s' INNER JOIN album al ON s.album_id = al.album_id WHERE s.status = 'approved' AND s.privacy = 'public'"%(uid)
        favoritesongdata=select(q)
        data['favoritesongdata']=favoritesongdata
        trendingsongdata=get_song_data(uid)
        data['trendingsongdata']=trendingsongdata
        q="SELECT p.playlist_id,p.playlist_name,p.image_loc,p.status FROM playlist p INNER JOIN playlisttrack pt ON p.playlist_id=pt.playlist_id WHERE p.type='public' AND p.status='active' GROUP BY pt.playlist_id"
        publicplaylistdata=select(q)
        data['publicplaylistdata']=publicplaylistdata
        return render_template('user/home.html', data=data)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))
    
@user.route('/favorite')
def favorite():
    if 'uid' in session:
        uid=session['uid']
        data={}
        q="select * from user where user_id='%s'"%(uid)
        res=select(q)
        data['userdetails']=res[0]
        q="SELECT DISTINCT al.album_id, al.album_name, al.image_loc, al.cover_pic FROM album al INNER JOIN songs s ON al.album_id = s.album_id INNER JOIN likes l ON al.album_id = l.content_id AND l.content_type = 'album' WHERE s.privacy = 'public' AND s.status = 'approved' AND l.user_id = '%s'"%(uid)
        favoritealbumdata=select(q)
        data['favoritealbumdata']=favoritealbumdata # trending albums (currently all albums. Needs to create a view for top 5 trending albums)
        q="SELECT DISTINCT ar.artist_id, ar.artist_name, ar.image_loc AS artist_image_loc, ar.cover_pic AS artist_cover_pic FROM artist ar INNER JOIN songartist sa ON ar.artist_id = sa.artist_id INNER JOIN songs s ON sa.song_id = s.song_id INNER JOIN likes l ON ar.artist_id = l.content_id AND l.content_type = 'artist' WHERE s.privacy = 'public' AND s.status = 'approved' AND l.user_id = '%s' GROUP BY ar.artist_id"%(uid)
        favoriteartistdata=select(q)
        data['favoriteartistdata']=favoriteartistdata
        q="SELECT s.song_id, s.song_name, al.album_name, s.image_loc AS song_image_loc, s.song_loc, s.genre, s.language, s.duration, CASE WHEN l.content_id IS NOT NULL THEN 'yes' ELSE 'no' END AS liked FROM songs s INNER JOIN likes l ON s.song_id = l.content_id AND l.content_type = 'song' AND l.user_id = '%s' INNER JOIN album al ON s.album_id = al.album_id WHERE s.status = 'approved' AND s.privacy = 'public'"%(uid)
        favoritesongdata=select(q)
        data['favoritesongdata']=favoritesongdata
        return render_template('user/favorite.html', data=data)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))
    
@user.route('/playlist', methods=['GET','POST'])
def playlist():
    if 'uid' in session:
        uid=session['uid']
        data={}
        q="select * from user where user_id='%s'"%(uid)
        res=select(q)
        data['userdetails']=res[0]
        q="select * from playlist where user_id='%s' and status='active'"%(uid)
        playlistdata=select(q)
        data['playlistdata']=playlistdata
        q="SELECT p.playlist_id,p.playlist_name,p.image_loc,p.status FROM playlist p INNER JOIN playlisttrack pt ON p.playlist_id=pt.playlist_id WHERE p.type='public' AND p.status='active' GROUP BY pt.playlist_id"
        publicplaylistdata=select(q)
        data['publicplaylistdata']=publicplaylistdata
        if 'CreatePlaylistBtn' in request.form:
            # CreatePlaylistBtn is clicked
            playlist_name = request.form.get('playlist_name')
            q="insert into playlist(playlist_name,image_loc,user_id,status,type) values ('%s','null','%s','active','private')"%(playlist_name,uid)
            pid=insert(q)
            if pid > 0:
                playlist_image = request.files['image_file']
                UpdatePlaylistImage(playlist_image,pid)
                flash("success: Playlist created successfully")
                return redirect(url_for('user.playlist'))
            
        return render_template('user/playlist.html', data=data)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))
    
@user.route('/search', methods=['POST'])
def search():
    search_text = request.form.get('text')
    q = "SELECT s.song_id, s.song_name,GROUP_CONCAT(ar.artist_name SEPARATOR ', ') AS artist_name, s.song_loc, s.image_loc, s.genre, s.language, s.duration FROM songs s INNER JOIN songartist sar ON s.song_id = sar.song_id INNER JOIN artist ar ON sar.artist_id = ar.artist_id WHERE s.privacy = 'public' AND s.status = 'approved' GROUP BY s.song_id"
    songs = select(q)

    q = "SELECT al.album_id,al.album_name,al.image_loc,al.cover_pic,COUNT(s.song_id) AS songs  FROM album al INNER JOIN songs s ON al.album_id=s.album_id AND s.privacy='public' AND s.status='approved' GROUP BY al.album_id"
    albums = select(q)

    q = "SELECT ar.artist_id,ar.artist_name,ar.image_loc,ar.cover_pic, COUNT(s.song_id) AS songs FROM artist ar INNER JOIN songartist sar ON ar.artist_id=sar.artist_id INNER JOIN songs s ON sar.song_id=s.song_id AND  s.privacy='public' AND s.status='approved' GROUP BY ar.artist_id"
    artists = select(q)

    # Find the matches above a certain similarity threshold for song names
    threshold = 80  # Adjust the threshold as needed
    song_matches = process.extract(search_text, [song['song_name'] for song in songs], limit=5)
    matching_songs = []
    for song in songs:
        for match in song_matches:
            if match[0] == song['song_name'] and match[1] >= threshold:
                song['score'] = match[1]
                matching_songs.append(song)
                break

    # Sort matching songs by score in descending order
    matching_songs = sorted(matching_songs, key=lambda x: x['score'], reverse=True)

    # Find the matches above a certain similarity threshold for album names
    album_matches = process.extract(search_text, [album['album_name'] for album in albums], limit=5)
    matching_albums = []
    for album in albums:
        for match in album_matches:
            if match[0] == album['album_name'] and match[1] >= threshold:
                album['score'] = match[1]
                matching_albums.append(album)
                break

    # Sort matching albums by score in descending order
    matching_albums = sorted(matching_albums, key=lambda x: x['score'], reverse=True)

    # Find the matches above a certain similarity threshold for artist names
    artist_matches = process.extract(search_text, [artist['artist_name'] for artist in artists], limit=5)
    matching_artists = []
    for artist in artists:
        for match in artist_matches:
            if match[0] == artist['artist_name'] and match[1] >= threshold:
                artist['score'] = match[1]
                matching_artists.append(artist)
                break

    # Sort matching artists by score in descending order
    matching_artists = sorted(matching_artists, key=lambda x: x['score'], reverse=True)

    response = {
        'matching_songs': matching_songs,
        'matching_albums': matching_albums,
        'matching_artists': matching_artists
    }

    return jsonify(response)


@user.route('/play', methods=['POST'])
def play():
    if 'uid' in session:
        contenttype= request.form['contenttype']
        uid = session['uid']
        data = {}
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        data['currentalbumsongs']=''
        data['currentartistsongs']=''
        data['favoritesongdata']=''
        data['songdata']=''
        q="select * from playlist where status='active' and user_id='%s'"%(uid)
        playlistdata=select(q)
        data['playlistdata']=playlistdata
        playlistname={}
        if contenttype == 'album':
            album_id= request.form['album_id']
            # Adding to clicks table
            q="INSERT INTO clicks(content_id,user_id,content_type) values ('%s','%s','album')"%(album_id,uid)
            cid=insert(q)
            q="SELECT al.album_id, al.album_name, al.image_loc, al.cover_pic, (CASE WHEN l.content_id IS NOT NULL THEN 'yes' ELSE 'no' END) AS liked FROM album al LEFT JOIN likes l ON al.album_id = l.content_id AND l.content_type = 'album' AND l.user_id='%s' WHERE al.album_id = '%s'"%(uid,album_id)
            albumdetails=select(q)
            album_name = albumdetails[0]['album_name']
            album_img = albumdetails[0]['image_loc']
            album_cover = albumdetails[0]['cover_pic']
            album_like = albumdetails[0]['liked']
            q="SELECT s.song_id, s.song_name, s.image_loc AS song_image_loc, s.song_loc, s.genre, s.LANGUAGE, s.duration, al.album_name, CASE WHEN l.content_id IS NOT NULL THEN 'yes' ELSE 'no' END AS liked FROM songs s INNER JOIN album al USING (album_id) LEFT JOIN likes l ON s.song_id = l.content_id AND l.user_id = '%s' AND l.content_type='song' WHERE s.privacy = 'public' AND s.STATUS = 'approved' AND al.album_id = '%s';"%(uid,album_id)
            currentalbumsongs=select(q)
            data['currentalbumsongs']=currentalbumsongs
            playlistname['name']=album_name
            playlistname['main_pic']=album_img
            playlistname['cover_pic']=album_cover
            playlistname['id']=album_id
            playlistname['like']=album_like
        elif contenttype=='artist':
            artist_id=request.form['artist_id']
            q="INSERT INTO clicks(content_id,user_id,content_type) values ('%s','%s','artist')"%(artist_id,uid)
            cid=insert(q)
            q="SELECT ar.artist_id, ar.artist_name, ar.image_loc,ar.cover_pic, (CASE WHEN l.content_id IS NOT NULL THEN 'yes' ELSE 'no' END) AS liked FROM artist ar LEFT JOIN likes l ON ar.artist_id = l.content_id AND l.content_type = 'artist' AND l.user_id='%s' WHERE ar.artist_id = '%s'"%(uid,artist_id)
            artistdetails=select(q)
            artist_name = artistdetails[0]['artist_name']
            artist_img = artistdetails[0]['image_loc']
            artist_cover = artistdetails[0]['cover_pic']
            artist_like = artistdetails[0]['liked']
            q="SELECT s.song_id, s.song_name, s.image_loc AS song_image_loc, s.song_loc, s.genre, s.LANGUAGE, s.duration, al.album_name, CASE WHEN l.content_id IS NOT NULL THEN 'yes' ELSE 'no' END AS liked FROM songs s INNER JOIN songartist sar USING (song_id) INNER JOIN artist ar ON ar.artist_id = sar.artist_id INNER JOIN album al USING (album_id) LEFT JOIN likes l ON s.song_id = l.content_id AND l.user_id = '%s' AND l.content_type='song' WHERE s.privacy = 'public' AND s.STATUS = 'approved' AND ar.artist_id = '%s'"%(uid,artist_id)
            currentartistsongs=select(q)
            data['currentartistsongs']=currentartistsongs
            playlistname['name']=artist_name
            playlistname['main_pic']=artist_img
            playlistname['cover_pic']=artist_cover
            playlistname['id']=artist_id
            playlistname['like']=artist_like
        elif contenttype=='favoritesongs':
            q="SELECT s.song_id, s.song_name, al.album_name, s.image_loc AS song_image_loc, s.song_loc, s.genre, s.language, s.duration, CASE WHEN l.content_id IS NOT NULL THEN 'yes' ELSE 'no' END AS liked FROM songs s INNER JOIN likes l ON s.song_id = l.content_id AND l.content_type = 'song' AND l.user_id = '%s' INNER JOIN album al ON s.album_id = al.album_id WHERE s.status = 'approved' AND s.privacy = 'public'"%(uid)
            favoritesongdata=select(q)
            data['favoritesongdata']=favoritesongdata
        elif contenttype == 'trendingsongs':
            trendingsongdata=get_song_data(uid)
            data['trendingsongdata']=trendingsongdata
        elif contenttype == 'SearchSong':
            # Render the template and pass the necessary data
            song_id=request.form['song_id']
            q="INSERT INTO clicks(content_id,user_id,content_type) values ('%s','%s','song')"%(song_id,uid)
            cid=insert(q)
            q="SELECT s.song_id, s.song_name, al.album_name, s.image_loc AS song_image_loc, s.song_loc, s.genre, s.language, s.duration, CASE WHEN l.content_id IS NOT NULL THEN 'yes' ELSE 'no' END AS liked FROM songs s INNER JOIN likes l ON s.song_id = l.content_id AND l.content_type = 'song' AND l.user_id = '%s' INNER JOIN album al ON s.album_id = al.album_id WHERE s.song_id='%s'"%(uid,song_id)
            searchsongdata=select(q)
            data['searchsongdata']=searchsongdata
        elif contenttype == 'SongCategories':
            q=''
            content_name = request.form.get('content_name')
            category_type = request.form.get('category_type')
            if category_type == 'language':
                q="SELECT s.song_id, s.song_name, al.album_name, s.image_loc AS song_image_loc, s.song_loc, s.genre, s.language, s.duration, CASE WHEN l.content_id IS NOT NULL THEN 'yes' ELSE 'no' END AS liked FROM songs s LEFT JOIN likes l ON s.song_id = l.content_id AND l.content_type = 'song' AND l.user_id = '%s' INNER JOIN album al ON s.album_id = al.album_id WHERE s.language='%s' and s.status='approved' and s.privacy='public'"%(uid,content_name)
            elif category_type == 'genre':
                q="SELECT s.song_id, s.song_name, al.album_name, s.image_loc AS song_image_loc, s.song_loc, s.genre, s.language, s.duration, CASE WHEN l.content_id IS NOT NULL THEN 'yes' ELSE 'no' END AS liked FROM songs s LEFT JOIN likes l ON s.song_id = l.content_id AND l.content_type = 'song' AND l.user_id = '%s' INNER JOIN album al ON s.album_id = al.album_id WHERE s.genre='%s' and s.status='approved' and s.privacy='public';"%(uid,content_name)
            songcategorydata=select(q)
            data['songcategorydata']=songcategorydata
            data['songcategorytype']={'name':content_name}
            
        return render_template('user/playarea.html', data=data, playlist=playlistname)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))


@user.route('/playlist_play', methods=['POST'])
def playlist_play():
    if 'uid' in session:
        contenttype= request.form['contenttype']
        uid = session['uid']
        data = {}
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        data['currentalbumsongs']=''
        data['currentartistsongs']=''
        data['favoritesongdata']=''
        data['songdata']=''
        q="select * from playlist where status='active' and user_id='%s'"%(uid)
        playlistdata=select(q)
        data['playlistdata']=playlistdata
        playlistname={}
        if contenttype == 'userplaylist':
            playlist_id= request.form['playlist_id']
            q="select * from playlist where playlist_id='%s'"%(playlist_id)
            albumdetails=select(q)
            playlist_name = albumdetails[0]['playlist_name']
            playlist_img = albumdetails[0]['image_loc']
            q="SELECT s.song_id, s.song_name, s.image_loc AS song_image_loc, s.song_loc, s.genre, s.LANGUAGE, s.duration, al.album_name, CASE WHEN l.content_id IS NOT NULL THEN 'yes' ELSE 'no' END AS liked FROM songs s INNER JOIN album al USING (album_id) INNER JOIN playlisttrack pt ON s.song_id=pt.song_id AND pt.playlist_id='%s'  LEFT JOIN likes l ON s.song_id = l.content_id AND l.user_id = '%s' AND l.content_type='song' WHERE s.privacy = 'public' AND s.STATUS = 'approved';"%(playlist_id,uid)
            playlistsongs=select(q)
            data['playlistsongs']=playlistsongs
            playlistname['name']=playlist_name
            playlistname['main_pic']=playlist_img
            
        return render_template('user/playlistplayarea.html', data=data, playlist=playlistname)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@user.route('/song_click', methods=['POST'])
def song_click():
    if 'uid' in session:
        uid = session['uid']
        song_id = request.json['song_id']
        song_index = request.json['song_index']
        q="INSERT INTO clicks(content_id,user_id,content_type) values ('%s','%s','song')"%(song_id,uid)
        cid=insert(q)
        response = {
            'status': 'success',
            'message': 'Song ID and song index received',
            'song_id': song_id,
            'song_index': song_index
        }
        
        # Return the response as JSON
        return jsonify(response)

@user.route('/explore' , methods=['GET', 'POST'])
def explore():
    if 'uid' in session:
        uid=session['uid']
        data={}
        q="select * from user where user_id='%s'"%(uid)
        res=select(q)
        data['userdetails']=res[0]
        categories=get_categories_data()
        data['categories']=categories
        if request.method == 'POST':
            song_name = request.form.get('song_name')
            content_type = request.form.get('content_type')
            return song_name
        return render_template('user/explore.html', data=data)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@user.route('/profile')
def profile():
    if 'uid' in session:
        uid=session['uid']
        data={}
        q="select * from user inner join login using (login_id) where user_id='%s'"%(uid)
        res=select(q)
        data['userdetails']=res[0]
        return render_template('user/profile.html', data=data)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@user.route('/edit_profile' , methods=['GET', 'POST'])
def edit_profile():
    if 'uid' in session:
        uid=session['uid']
        data={}
        q="select * from user where user_id='%s'"%(uid)
        res=select(q)
        data['userdetails']=res[0]
        return render_template('user/edit_profile.html', data=data)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@user.route('/update_profile', methods=['POST'])
def update_profile():
    if 'uid' in session:
        uid = session['uid']
        q = "SELECT * FROM user WHERE user_id='%s'" % uid
        res = select(q)
        data = {}
        data['userdetails'] = res[0]
        fname = request.form['upfname']
        lname = request.form['uplname']
        mob = request.form['upmob']
        email=request.form['upemail']
        q = "UPDATE user SET fname='%s', lname='%s', mobile='%s',email='%s' WHERE user_id='%s'" % (fname, lname, mob,email, uid)
        update(q)
        flash("success: Update successful")  # Generate flash message
        return redirect(url_for('user.profile'))
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@user.route('/propicupload', methods=['POST'])
def propicupload():
    if 'uid' in session:
        uid = session['uid']
        q = "SELECT * FROM user WHERE user_id='%s'" %(uid)
        res = select(q)
        data={}
        data['userdetails']=res[0]
        image = request.files['image']
        if image.filename != '':
            UpdateProfileImage(image,uid)
            flash("success: Successfully updated image")
        else:
            flash("danger: Please select an image first")
        return redirect(url_for('user.edit_profile'))
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@user.route('/deletepropic', methods=['POST','GET'])
def deletepropic():
    if 'uid' in session:
        uid = session['uid']
        DeleteProfileImage(uid)
        flash("warning: Profile Picture Deleted Successfully.")
        return redirect(url_for('user.edit_profile'))
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@user.route('/edit_playlist', methods=['GET','POST'])
def edit_playlist():
    if 'uid' in session:
        uid = session['uid']
        q = "SELECT * FROM user WHERE user_id='%s'" %(uid)
        res = select(q)
        data={}
        data['userdetails']=res[0]
        if 'playlist_id' in request.form:
            playlist_id=request.form['playlist_id']
        else:
            playlist_id= session['playlist_id']
        session['playlist_id']=playlist_id
        q="select * from playlist where playlist_id='%s'"%(playlist_id)
        playlistdata=select(q)
        data['playlistdata']=playlistdata[0]
        q="select * from playlisttrack pt inner join songs s on pt.song_id=s.song_id and pt.playlist_id='%s' inner join album al on s.album_id=al.album_id"%(playlist_id)
        playlistsongs=select(q)
        data['playlistsongs']=playlistsongs
        if 'UpdatePlaylistName' in request.form:
            playlist_name=request.form['uppname']
            q="update playlist set playlist_name='%s' where playlist_id='%s'"%(playlist_name,playlist_id)
            update(q)
            flash("success: Name Updated Successfully")
            return redirect(url_for('user.edit_playlist'))
        if 'UpdatePlaylistImage' in request.form:
            playlist_image = request.files['update_image_file']
            UpdatePlaylistImage(playlist_image,playlist_id)
            flash("success: Image Updated successfully")
            return redirect(url_for('user.edit_playlist'))
        if 'DeletePlaylistBtn' in request.form:
            message=deletePlaylist(playlist_id)
            flash(message)
            return redirect(url_for('user.playlist'))
        if 'SongRemove' in request.form:
            song_id=request.form['song_id']
            playlist_id=request.form['playlist_id']
            q="delete from playlisttrack where playlist_id='%s' and song_id='%s'"%(playlist_id,song_id)
            delete(q)
            flash("warning: Song Deleted Successfully.")
            return redirect(url_for('user.edit_playlist'))
        return render_template('user/edit_playlist.html', data=data)
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@user.route('/changepassword', methods=['GET', 'POST'])
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
        return redirect(url_for('user.profile'))
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))

@user.route('/disable_profile', methods=['GET', 'POST'])
def disable_profile():
    if 'uid' in session:
        login_id = session['login_id']
        uid = session['uid']
        q="update user set status='deactive' where user_id='%s'"%(uid)
        update(q)
        subject="User Dectivation"
        message="Your account have deactivated your account successfully. Contact admin if you feels to reactivate."
        send_email(uid,subject,message)
        return redirect(url_for('user.logout'))
    else:
        flash("danger: Session Unavailable. Login Again")
        return redirect(url_for('public.home'))
    
@user.route('/like_song', methods=['POST'])
def like_song():
    if 'uid' in session:
        uid = session['uid']
        song_id = request.form.get('songId')
        is_liked = request.form.get('isLiked')
        # Perform the necessary actions based on the song ID and like status
        if is_liked == 'true':
            q="insert into likes(content_id,user_id,content_type) values('%s','%s','song')"%(song_id,uid)
            likeid=insert(q)
        else:
            q="delete from likes where content_id='%s' and user_id='%s' and content_type='song'"%(song_id,uid)
            delete(q)

        # Return a JSON response indicating success
        return jsonify({'message': 'Like/Unlike action successful'})
    
@user.route('/like_album', methods=['POST'])
def like_album():
    if 'uid' in session:
        uid = session['uid']
        album_id = request.form.get('albumId')  # Get the album ID from the request form
        is_liked = request.form.get('isLiked')  # Get the like status from the request form

        # Perform the necessary actions based on the song ID and like status
        if is_liked == 'true':
            q="insert into likes(content_id,user_id,content_type) values('%s','%s','album')"%(album_id,uid)
            likeid=insert(q)
        else:
            q="delete from likes where content_id='%s' and user_id='%s' and content_type='album'"%(album_id,uid)
            delete(q)

        # Return a JSON response indicating success
        return jsonify({'message': 'Like/Unlike action successful'})
    
@user.route('/like_artist', methods=['POST'])
def like_artist():
    if 'uid' in session:
        uid = session['uid']
        artist_id = request.form.get('artistId')  # Get the artist ID from the request form
        is_liked = request.form.get('isLiked')  # Get the like status from the request form

        # Perform the necessary actions based on the song ID and like status
        if is_liked == 'true':
            q="insert into likes(content_id,user_id,content_type) values('%s','%s','artist')"%(artist_id,uid)
            likeid=insert(q)
        else:
            q="delete from likes where content_id='%s' and user_id='%s' and content_type='artist'"%(artist_id,uid)
            delete(q)

        # Return a JSON response indicating success
        return jsonify({'message': 'Like/Unlike action successful'})

@user.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    data = request.json
    playlist_id = data.get('playlistId')
    song_id = data.get('songId')
    q="select * from playlisttrack where playlist_id='%s' and song_id='%s'"%(playlist_id,song_id)
    playlisttrack=select(q)
    if len(playlisttrack) == 0:
        q="insert into playlisttrack(playlist_id,song_id) values ('%s','%s')"%(playlist_id,song_id)
        ptid=insert(q)
        if ptid > 0:
            return jsonify(message='Song added to playlist'), 200
    else:
        return jsonify(message='Song already in the playlist'), 400


@user.route('/logout')
def logout():
    session.clear()
    flash("warning: You have logged out")
    return redirect(url_for('public.home'))




