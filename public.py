from flask import *
from database import*


public=Blueprint('public',__name__)

@public.route('/')
def home():
    return render_template('public/index.html')
    

@public.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        u = request.form['uname']
        pa = request.form['pwd']
        q = "SELECT * FROM login WHERE username='%s' AND password='%s'" % (u, pa)
        res = select(q)

        if res:
            session['login_id'] = res[0]['login_id']
            lid = session['login_id']
            if res[0]['user_type'] == "admin":
                return redirect(url_for('admin.admin_home'))
            elif res[0]['user_type'] == "user":
                q = "SELECT * FROM user WHERE login_id='%s'" % lid
                res = select(q)
                if res:
                    session['uid'] = res[0]['user_id']
                    return redirect(url_for('user.user_home'))
        else:
            # Password doesn't match or user doesn't exist
            flash('Invalid username or password')
            return redirect(url_for('public.home'))

    # Render the login page (GET request) or redirect to another page (POST request)
    return render_template('Public/index.html')


@public.route('/signup', methods=['POST', 'GET'])
def signup():
        first_name = request.form['regfname']
        last_name = request.form['reglname']
        email = request.form['regemail']
        mobile_number = request.form['regmobile']
        password = request.form['regpass1']
        cnfpassword = request.form['regpass2']
        
        q="select * from login where username='%s'"%(email,)
        res=select(q)
        if res:
            flash('Username already exist')
        else:
            q="insert into login (username,password,user_type,status) values ('%s', '%s','%s','active')"%(email,password,'user')
            id=insert(q)
            q="insert into user (login_id,fname,lname,email,mobile,image_loc,status) values ('%s','%s','%s','%s','%s','null','active')"%(id,first_name,last_name,email,mobile_number)
            v=insert(q)
            if v:
                flash('Insertion Successfull')
        return redirect(url_for('public.home')) 
