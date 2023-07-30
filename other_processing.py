from database import *
import os
def UpdatePlaylistImage(playlist_image,pid):
    playlist_image_extension = os.path.splitext(playlist_image.filename)[1]
    # Specify the path where you want to save the uploaded files
    upload_folder = 'static/uploads/playlist'  # Update the path according to your setup
    # Customize the filenames
    playlist_image_filename = str(pid) + playlist_image_extension
    # Saving the path for database
    playlistpath='uploads/playlist/' + str(pid) + playlist_image_extension
    # Save the uploaded files with the customized filenames
    playlist_image.save(os.path.join(upload_folder, playlist_image_filename))
    q="update playlist set image_loc='%s' where playlist_id='%s'"%(playlistpath,pid)
    update(q)

def UpdateProfileImage(image,uid):
    DeleteProfileImage(uid)
    image_extension = os.path.splitext(image.filename)[1]
    # Specify the path where you want to save the uploaded files
    upload_folder = 'static/uploads/playlist'  # Update the path according to your setup
    # Customize the filenames
    image_filename = str(uid) + image_extension
    # Saving the path for database
    playlistpath='uploads/users/' + str(uid) + image_extension
    # Save the uploaded files with the customized filenames
    image.save(os.path.join(upload_folder, image_filename))
    q="update user set image_loc='%s' where user_id='%s'"%(playlistpath,uid)
    update(q)

def DeleteProfileImage(uid):
    q="select image_loc from user where user_id='%s'"%(uid)
    userdetails=select(q)
    imagepath = userdetails[0]['image_loc']
    if imagepath != 'null':
        imagepath= 'static/'+imagepath
        if os.path.exists(imagepath):
            os.remove(imagepath)
