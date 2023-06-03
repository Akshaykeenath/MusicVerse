from flask import *
from database import *
import os

user = Blueprint('user',__name__)

@user.route('/user_home')
def user_home():
    if 'uid' in session:
        uid=session['uid']
        data={}
        q="select * from user where user_id='%s'"%(uid)
        res=select(q)
        data['userdetails']=res[0]
        q="SELECT DISTINCT album_id,album_name,al.image_loc,al.cover_pic FROM songs s INNER JOIN album al USING (album_id) WHERE privacy='public' AND STATUS='approved'"
        albumdata=select(q)
        data['albumdata']=albumdata # trending albums (currently all albums. Needs to create a view for top 5 trending albums)
        q="SELECT s.song_id,song_name,s.image_loc AS song_image_loc, song_loc,genre,LANGUAGE,duration,ar.artist_id, ar.artist_name, ar.image_loc AS artist_image_loc, ar.cover_pic AS artist_cover_pic FROM songs s INNER JOIN artist ar USING (artist_id) WHERE s.privacy='public' AND s.STATUS='approved' GROUP BY ar.artist_id"
        artistdata=select(q)
        data['artistdata']=artistdata
        return render_template('user/home.html', data=data)
    else:
        return redirect(url_for('public.home'))
        

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
        playlistname={}
        if contenttype == 'album':
            album_id= request.form['album_id']
            album_name= request.form['album_name']
            album_img= request.form['album_img']
            album_cover= request.form['album_cover']
            q="SELECT al.album_id,s.song_id,artist_id,song_name,s.image_loc AS song_image_loc, song_loc,genre,LANGUAGE,user_id,privacy,duration,s.status,album_name,al.image_loc AS album_image_loc, al.cover_pic AS album_cover_pic FROM songs s INNER JOIN album al USING (album_id) WHERE s.privacy='public' AND s.STATUS='approved' AND album_id='%s'"%(album_id)
            currentalbumsongs=select(q)
            data['currentalbumsongs']=currentalbumsongs
            playlistname['name']=album_name
            playlistname['main_pic']=album_img
            playlistname['cover_pic']=album_cover
        if contenttype=='artist':
            artist_id=request.form['artist_id']
            artist_name= request.form['artist_name']
            artist_img= request.form['artist_img']
            artist_cover= request.form['artist_cover']
            q="SELECT s.song_id,song_name,s.image_loc AS song_image_loc, song_loc,genre,LANGUAGE,duration,ar.artist_id, ar.artist_name, ar.image_loc AS artist_image_loc, ar.cover_pic AS artist_cover_pic, al.album_name FROM songs s INNER JOIN artist ar USING (artist_id) INNER JOIN album al USING (album_id) WHERE s.privacy='public' AND s.STATUS='approved' AND ar.artist_id='%s'"%(artist_id)
            currentartistsongs=select(q)
            data['currentartistsongs']=currentartistsongs
            playlistname['name']=artist_name
            playlistname['main_pic']=artist_img
            playlistname['cover_pic']=artist_cover
        return render_template('user/playarea.html', data=data, playlist=playlistname)
    else:
        return redirect(url_for('public.home'))




@user.route('/recommendation')
def recommendation():
    if 'uid' in session:
        uid=session['uid']
        data={}
        q="select * from user where user_id='%s'"%(uid)
        res=select(q)
        data['userdetails']=res[0]
        return render_template('user/recommendation.html', data=data)
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
        print(data['userdetails'])
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
        print(data['userdetails'])
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
        return render_template('user/edit_profile.html',data=data)
    else:
        return redirect(url_for('public.home'))

@user.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('public.home'))




