from flask import *
from database import*
from other_functions import *
data={} 
public=Blueprint('public',__name__)

@public.route('/')
def home():
    return render_template('public/index.html',data=data)

@public.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        u = request.form['uname']
        pa = request.form['pwd']
        q = "SELECT * FROM login WHERE username='%s' AND password='%s'" % (u, pa)
        res = select(q)

        if res[0]['password'] == pa:
            session['login_id'] = res[0]['login_id']
            lid = session['login_id']
            if res[0]['user_type'] == "admin":
                return redirect(url_for('admin.admin_home'))
            elif res[0]['user_type'] == "user":
                q = "SELECT * FROM user WHERE login_id='%s'" % lid
                res = select(q)
                if res:
                    if res[0]['status'] == 'active':
                        session['uid'] = res[0]['user_id']
                        return redirect(url_for('user.user_home'))
                    else:
                        flash('danger: User Deactivated. Contact Administrator')
                        return redirect(url_for('public.home'))
        else:
            # Password doesn't match or user doesn't exist
            flash('danger: Invalid username or password')
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
        
        q="select * from login where username='%s'"%(email,)
        res=select(q)
        if res:
            flash('warning: Username already exist')
        else:
            q="insert into login (username,password,user_type,status) values ('%s', '%s','%s','active')"%(email,password,'user')
            id=insert(q)
            q="insert into user (login_id,fname,lname,email,mobile,image_loc,status) values ('%s','%s','%s','%s','%s','null','active')"%(id,first_name,last_name,email,mobile_number)
            v=insert(q)
            if v:
                flash('success: Insertion Successfull')
        return redirect(url_for('public.home')) 


@public.route('/verification', methods=['POST', 'GET'])
def verification():
    email = request.form['verifyemail']
    q="select * from user where email='%s'"%(email)
    uid=select(q)
    if len(uid) > 0:
        flash("danger: Email already exists. Select login")
        return redirect(url_for('public.home')) 
    else:
        send_otp(email)
        data={
            'email': email
        }
        return render_template('Public/index.html',value='otpmodal',data=data)

@public.route('/validation', methods=['POST', 'GET'])
def validation():
    otp = request.form['validateotp']
    email = request.form['validateemail']
    send_otp(email)
    data={
        'email': email
    }
    if is_valid_otp(otp):
        return render_template('Public/index.html',value='signupmodal',data=data)
    else:
        flash("danger: OTP is invalid. Try again.")
        return redirect(url_for('public.home')) 
    
@public.route('/forgotpassword', methods=['POST', 'GET'])
def forgotpassword():
    mob = request.form['verifymobile']
    email = request.form['verifyemail']
    q="select * from user where mobile='%s' and email='%s'"%(mob,email)
    userdet=select(q)
    if len(userdet)>0 :
        login_id=userdet[0]['login_id']
        q="select password from login where login_id='%s'"%(login_id)
        passwords=select(q)
        send_password(passwords[0]['password'],email)
        flash("success: Password send to registered mail id")
        return redirect(url_for('public.home')) 
    else:
        flash("danger: Invalid mail id or mobile number")
        return redirect(url_for('public.home')) 