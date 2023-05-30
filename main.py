from flask import Flask, render_template
from public import public
from admin import admin
from user import user
from uploader import uploader

app=Flask(__name__)

app.secret_key='key'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

app.register_blueprint(public)
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(user,url_prefix='/user')
app.register_blueprint( uploader,url_prefix='/uploader')

app.run(debug=True,port=5002,host="0.0.0.0")
