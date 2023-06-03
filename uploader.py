from flask import *
import os
from werkzeug.utils import secure_filename
from database import *
import uuid
from mutagen.mp3 import MP3

uploader =Blueprint('uploader',__name__)

@uploader.route('/')
def home():
    if 'uid' in session:
        uid = session['uid']
        song_id = request.form.get('song_id')
        print(song_id)
        data = {}
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        print(song_id)  # Print the song ID for testing
        return render_template('uploader/home.html', data=data)
    else:
        return redirect(url_for('public.home'))

@uploader.route('/allsongs' , methods=['GET', 'POST'])
def allsongs():
    if 'uid' in session:
        uid = session['uid']
        data = {}
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        q="SELECT s.song_id,s.song_name,al.album_name,ar.artist_name,s.date,s.status FROM songs s, artist ar, album al WHERE ar.artist_id=s.artist_id AND al.album_id=s.album_id AND s.user_id ='%s'"%(uid)
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
            q="SELECT s.song_id,s.song_name,al.album_id,al.album_name,ar.artist_id,ar.artist_name,s.date,s.image_loc,s.song_loc,s.genre,s.language,s.privacy FROM songs s, artist ar, album al WHERE ar.artist_id=s.artist_id AND al.album_id=s.album_id AND s.song_id='%s'"%(song_id)
            currentsongdata=select(q)
            print('Song id =',song_id)
            data['currentsongdata']=currentsongdata[0]
            if action.startswith('update_song'):
                return render_template('uploader/all_songs.html', data=data, value='updatesong')
            elif action.startswith('view_song'):
                 return render_template('uploader/all_songs.html', data=data, value='viewsong')
            elif action.startswith('delete_song'):
                # Delete song action
                # Handle the delete song functionality
                return 'Delete Song'
        return render_template('uploader/all_songs.html', data=data)
    else:
        return redirect(url_for('public.home'))

@uploader.route('/approvedsongs' , methods=['GET', 'POST'])
def approvedsongs():
    if 'uid' in session:
        uid = session['uid']
        data = {}
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        q="SELECT s.song_id,s.song_name,al.album_name,ar.artist_name,s.date FROM songs s, artist ar, album al WHERE ar.artist_id=s.artist_id AND al.album_id=s.album_id AND s.status='approved' AND s.privacy='public' AND s.user_id ='%s'"%(uid)
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
                q="SELECT s.song_id,s.song_name,al.album_id,al.album_name,ar.artist_id,ar.artist_name,s.date,s.image_loc,s.song_loc,s.genre,s.language,s.privacy FROM songs s, artist ar, album al WHERE ar.artist_id=s.artist_id AND al.album_id=s.album_id AND s.status='approved' AND s.privacy='public' AND s.song_id='%s'"%(song_id)
                currentsongdata=select(q)
                print('Song id =',song_id)
                data['currentsongdata']=currentsongdata[0]
                if action.startswith('update_song'):
                    return render_template('uploader/approved_songs.html', data=data, value='updatesong')
                elif action.startswith('view_song'):
                    return render_template('uploader/approved_songs.html', data=data, value='viewsong')
                elif action.startswith('delete_song'):
                    # Delete song action
                    # Handle the delete song functionality
                    return 'Delete Song'

        return render_template('uploader/approved_songs.html', data=data)
    else:
        return redirect(url_for('public.home'))

@uploader.route('/pendingsongs' , methods=['GET', 'POST'])
def pendingsongs():
    if 'uid' in session:
        uid = session['uid']
        data = {}
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        q="SELECT s.song_id,s.song_name,al.album_name,ar.artist_name,s.date FROM songs s, artist ar, album al WHERE ar.artist_id=s.artist_id AND al.album_id=s.album_id AND s.status='pending' AND s.privacy='public' AND s.user_id ='%s'"%(uid)
        pendingsongdata=select(q)
        data['pendingsongdata']=pendingsongdata
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
                q="SELECT s.song_id,s.song_name,al.album_id,al.album_name,ar.artist_id,ar.artist_name,s.date,s.image_loc,s.song_loc,s.genre,s.language,s.privacy FROM songs s, artist ar, album al WHERE ar.artist_id=s.artist_id AND al.album_id=s.album_id AND s.status='pending' AND s.privacy='public' AND s.song_id='%s'"%(song_id)
                currentsongdata=select(q)
                print('Song id =',song_id)
                data['currentsongdata']=currentsongdata[0]
                if action.startswith('update_song'):
                    return render_template('uploader/pending_songs.html', data=data, value='updatesong')
                elif action.startswith('view_song'):
                    return render_template('uploader/pending_songs.html', data=data, value='viewsong')
                elif action.startswith('delete_song'):
                    # Delete song action
                    # Handle the delete song functionality
                    return 'Delete Song'
        return render_template('uploader/pending_songs.html', data=data)
    else:
        return redirect(url_for('public.home'))

@uploader.route('/rejectedsongs')
def rejectedsongs():
    if 'uid' in session:
        uid = session['uid']
        data = {}
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        q="SELECT s.song_id,s.song_name,al.album_name,ar.artist_name,s.date FROM songs s, artist ar, album al WHERE ar.artist_id=s.artist_id AND al.album_id=s.album_id AND s.status='rejected' AND s.user_id ='%s'"%(uid)
        rejectedsongdata=select(q)
        data['rejectedsongdata']=rejectedsongdata
        return render_template('uploader/rejected_songs.html', data=data)
    else:
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
            artist=request.form['artist']
            privacy=request.form['privacy']
            genre=request.form['genre']
            date=request.form['date']
            language=request.form['language']
            pagename=request.form['pagename']
            q="update songs set artist_id='%s', album_id='%s', song_name='%s', genre='%s', date='%s',language='%s', privacy='%s' where song_id='%s'"%(artist,album,songname,genre,date,language,privacy,songid)
            update(q)
            flash('success: Song Details updated successfully')
            if pagename == 'privatesongs':
                return redirect(url_for('uploader.privatesongs'))
            elif pagename == 'pendingsongs':
                return redirect(url_for('uploader.pendingsongs'))
            
        
    return redirect(url_for('uploader.allsongs'))


@uploader.route('/privatesongs' , methods=['GET', 'POST'])
def privatesongs():
    if 'uid' in session:
        uid = session['uid']
        data = {}
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        q="SELECT s.song_id,s.song_name,al.album_name,ar.artist_name,s.date FROM songs s, artist ar, album al WHERE ar.artist_id=s.artist_id AND al.album_id=s.album_id AND s.privacy='private' AND s.user_id ='%s'"%(uid)
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
                q="SELECT s.song_id,s.song_name,al.album_id,al.album_name,ar.artist_id,ar.artist_name,s.date,s.image_loc,s.song_loc,s.genre,s.language,s.privacy FROM songs s, artist ar, album al WHERE ar.artist_id=s.artist_id AND al.album_id=s.album_id AND s.privacy='private' AND s.song_id='%s'"%(song_id)
                currentsongdata=select(q)
                data['currentsongdata']=currentsongdata[0]
                if action.startswith('update_song'):
                    return render_template('uploader/private_songs.html', data=data, value='updatesong')
                elif action.startswith('view_song'):
                    return render_template('uploader/private_songs.html', data=data, value='viewsong')
                elif action.startswith('delete_song'):
                    # Delete song action
                    # Handle the delete song functionality
                    return 'Delete Song'


        return render_template('uploader/private_songs.html', data=data)
    else:
        return redirect(url_for('public.home'))
    

@uploader.route('/profile')
def profile():
    if 'uid' in session:
        uid = session['uid']
        data = {}
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        print(data['userdetails'])
        return render_template('uploader/uploader_profile.html', data=data)
    else:
        return redirect(url_for('public.home'))
    

@uploader.route('/artist', methods=['GET', 'POST'])
def artist():
    if 'uid' in session:
        uid = session['uid']
        data = {}
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        q = "select * from artist"
        artistdata=select(q)
        data['userdetails'] = res[0]
        data['artistdetails']=artistdata

        if request.method == 'POST':
            artistname = request.form['artistname']
            artist_image = request.files['image']
            cover_image = request.files['coverimage']

            # Get the file extensions
            artist_image_extension = os.path.splitext(artist_image.filename)[1]
            cover_image_extension = os.path.splitext(cover_image.filename)[1]

            # Specify the path where you want to save the uploaded files
            upload_folder = 'static/uploads/artist'  # Update the path according to your setup

            # Create the upload folder if it doesn't exist
            os.makedirs(upload_folder, exist_ok=True)

            # Customize the filenames
            artist_image_filename = artistname + 'propic' + artist_image_extension
            cover_image_filename = artistname + 'coverpic' + cover_image_extension

            # Saving the path for database
            profilepath='uploads/artist/' + artistname + 'propic' + artist_image_extension
            coverpath='uploads/artist/' + artistname + 'coverpic' + cover_image_extension


            # Save the uploaded files with the customized filenames
            artist_image.save(os.path.join(upload_folder, artist_image_filename))
            cover_image.save(os.path.join(upload_folder, cover_image_filename))

            # Saving to database
            q="insert into artist (artist_name,image_loc,cover_pic) values ('%s','%s','%s')"%(artistname,profilepath,coverpath)
            id=insert(q)
            if q :
                flash('success: Artist added successfully')
                return render_template('uploader/artist.html', data=data)
            else:
                flash('danger: Artist not added')
                return render_template('uploader/artist.html', data=data)
        return render_template('uploader/artist.html', data=data)
    else:
        return redirect(url_for('public.home'))
    

@uploader.route('/album', methods=['GET', 'POST'])
def album():
    if 'uid' in session:
        uid = session['uid']
        data = {}
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        q = "select * from album"
        albumdata=select(q)
        data['userdetails'] = res[0]
        data['albumdetails']=albumdata

        if request.method == 'POST':
            albumname = request.form['albumname']
            album_image = request.files['image']
            cover_image = request.files['coverimage']

            # Get the file extensions
            album_image_extension = os.path.splitext(album_image.filename)[1]
            cover_image_extension = os.path.splitext(cover_image.filename)[1]

            # Specify the path where you want to save the uploaded files
            upload_folder = 'static/uploads/album'  # Update the path according to your setup

            # Create the upload folder if it doesn't exist
            os.makedirs(upload_folder, exist_ok=True)

            # Customize the filenames
            album_image_filename = albumname + 'propic' + album_image_extension
            cover_image_filename = albumname + 'coverpic' + cover_image_extension

            # Saving the path for database
            profilepath='uploads/album/' + albumname + 'propic' + album_image_extension
            coverpath='uploads/album/' + albumname + 'coverpic' + cover_image_extension


            # Save the uploaded files with the customized filenames
            album_image.save(os.path.join(upload_folder, album_image_filename))
            cover_image.save(os.path.join(upload_folder, cover_image_filename))

            # Saving to database
            q="insert into album (album_name,image_loc,cover_pic) values ('%s','%s','%s')"%(albumname,profilepath,coverpath)
            id=insert(q)
            if q :
                flash('success: Album added successfully')
                return render_template('uploader/album.html', data=data)
            else:
                flash('danger: Album not added')
                return render_template('uploader/album.html', data=data)
        return render_template('uploader/album.html', data=data)
    else:
        return redirect(url_for('public.home'))



    
@uploader.route('/uploadmusic', methods=['GET', 'POST'])
def uploadmusic():
        if 'uid' in session:
            uid = session['uid']
            data = {}
            q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
            res = select(q)
            data['userdetails'] = res[0]
            if request.method == 'POST':
                file = request.files['file']
                if file and file.filename.endswith('.mp3'):
                    audio = MP3(file)
                    duration_in_seconds = str(int(audio.info.length))
                    file_extension = os.path.splitext(file.filename)[1]
                    songpath='uploads/songs/' +res[0]['fname']+str(uuid.uuid4()) + file_extension
                    file.save('static/'+songpath)
                    songpathdb='/static/'+songpath # To store in database with /static as it may sometimes conflict with the save if given in .save
                    session['songpath']=songpathdb
                    duration_in_min=secondstominute(int(duration_in_seconds))
                    session['songduration']=duration_in_min
                    print('static/'+songpath)
                    flash("Successfully saved the song. Duration :"+ duration_in_min)
                    return redirect(url_for('uploader.uploadsong'))
                else:
                    flash("Invalid file format. Please upload an MP3 file.")
                    return render_template('uploader/home.html', data=data)
            return render_template('uploader/home.html', data=data)
        

@uploader.route('/uploadsong', methods=['GET', 'POST'])
def uploadsong():
    if 'uid' in session:
        uid = session['uid']
        data = {}
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]        #A flash message is there for upload successfull in return render_template('uploader/home.html', data=data)
        q="select * from artist"
        artistdata=select(q)
        data['artistdata'] = artistdata
        q="select * from album"
        albumdata=select(q)
        data['albumdata']=albumdata
        if request.method == 'POST':
            songname=request.form['songname']
            image = request.files['image']
            album=request.form['album']
            artist=request.form['artist']
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
            q="insert into songs (artist_id,album_id,song_name,image_loc,song_loc,genre,date,language,user_id,privacy,duration,status) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(artist,album,songname,songimagepath,songpath,genre,date,language,uid,privacy,songduration,'pending')
            ins=insert(q)
            if ins:
                flash('success: Song uploaded successfully')
                if privacy == 'public':
                    return redirect(url_for('uploader.pendingsongs'))
                else:
                    return redirect(url_for('uploader.privatesongs'))
        return render_template('uploader/uploadsong.html', data=data)
    else:
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