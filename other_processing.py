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