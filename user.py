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
        print(data['userdetails'])
        return render_template('user/home.html', data=data)
    else:
        return redirect(url_for('public.home'))
        

@user.route('/play', methods=['POST'])
def play():
    if 'uid' in session:
        uid = session['uid']
        song_id = request.form.get('song_id')
        print(song_id)
        data = {}
        q = "SELECT * FROM user WHERE user_id='%s'" % (uid)
        res = select(q)
        data['userdetails'] = res[0]
        print(data['userdetails'])
        print(song_id)  # Print the song ID for testing
        return render_template('user/playarea.html', data=data)
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
        print(data['userdetails'])
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




