from flask import *
from database import *
import os
from trending import *
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

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
        return render_template('user/home.html', data=data)
    else:
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

            
        return render_template('user/playarea.html', data=data, playlist=playlistname)
    else:
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

@user.route('/explore')
def explore():
    if 'uid' in session:
        uid=session['uid']
        data={}
        q="select * from user where user_id='%s'"%(uid)
        res=select(q)
        data['userdetails']=res[0]
        return render_template('user/explore.html', data=data)
    else:
        return redirect(url_for('public.home'))

@user.route('/profile')
def profile():
    if 'uid' in session:
        uid=session['uid']
        data={}
        q="select * from user where user_id='%s'"%(uid)
        res=select(q)
        data['userdetails']=res[0]
        return render_template('user/profile.html', data=data)
    else:
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
        return redirect(url_for('public.home'))

app = Flask(__name__)

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
        q = "UPDATE user SET fname='%s', lname='%s', mobile='%s' WHERE user_id='%s'" % (fname, lname, mob, uid)
        update(q)
        flash("Update successful")  # Generate flash message
        return redirect(url_for('user.profile'))
    else:
        return redirect(url_for('public.home'))
    


@user.route('/propicupload', methods=['POST'])
def propicupload():
    if 'uid' in session:
        uid = session['uid']
        q = "SELECT * FROM user WHERE user_id='%s'" %(uid)
        res = select(q)
        data={}
        data['userdetails']=res[0]
        # Get the uploaded image file
        image = request.files['image']
        file_extension = os.path.splitext(image.filename)[1]
        # Save the image to a desired location
        imgpath='uploads/' +res[0]['fname']+res[0]['login_id'] + file_extension
        image.save('static/'+imgpath)
        q="update user set image_loc='%s' where user_id='%s'"%(imgpath,uid)
        insert(q)
        flash("Successfully updated image")
        return redirect(url_for('user.edit_profile'))
    else:
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


@user.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('public.home'))




