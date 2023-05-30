from flask import *

admin =Blueprint('admin',__name__)

@admin.route('/admin_home')
def admin_home():
    return render_template('admin/index.html')

