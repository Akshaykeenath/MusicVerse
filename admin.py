from flask import *
from database import*

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

@admin.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('public.home'))