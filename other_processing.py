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
    upload_folder = 'static/uploads/users'  # Update the path according to your setup
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

def updateAlbumCover(cover_image,albumid):
    deleteAlbumCover(albumid)
    cover_image_extension = os.path.splitext(cover_image.filename)[1]
    # Specify the path where you want to save the uploaded files
    upload_folder = 'static/uploads/album'  # Update the path according to your setup
    # Create the upload folder if it doesn't exist
    os.makedirs(upload_folder, exist_ok=True)
    # Customize the filenames
    cover_image_filename = str(albumid) + 'coverpic' + cover_image_extension
    # Saving the path for database
    coverpath='uploads/album/' + str(albumid) + 'coverpic' + cover_image_extension
    # Save the uploaded files with the customized filenames
    cover_image.save(os.path.join(upload_folder, cover_image_filename))
    # Saving to database
    q="update album set cover_pic='%s' where album_id='%s'"%(coverpath,albumid)
    update(q)

def deleteAlbumCover(albumid):
    q="select cover_pic from album where album_id='%s'"%(albumid)
    albumdetails=select(q)
    imagepath = albumdetails[0]['cover_pic']
    if imagepath != 'null':
        imagepath= 'static/'+imagepath
        if os.path.exists(imagepath):
            os.remove(imagepath)

def updateAlbumImage(album_image,albumid):
    deleteAlbumImage(albumid)
    # Get the file extensions
    album_image_extension = os.path.splitext(album_image.filename)[1]
    # Specify the path where you want to save the uploaded files
    upload_folder = 'static/uploads/album'  # Update the path according to your setup
    # Create the upload folder if it doesn't exist
    os.makedirs(upload_folder, exist_ok=True)
    # Customize the filenames
    album_image_filename = str(albumid) + 'propic' + album_image_extension
    # Saving the path for database
    profilepath='uploads/album/' + str(albumid) + 'propic' + album_image_extension
    # Save the uploaded files with the customized filenames
    album_image.save(os.path.join(upload_folder, album_image_filename))
    # Saving to database
    q="update album set image_loc='%s' where album_id='%s'"%(profilepath,albumid)
    update(q)

def deleteAlbumImage(albumid):
    q="select image_loc from album where album_id='%s'"%(albumid)
    albumdetails=select(q)
    imagepath = albumdetails[0]['image_loc']
    if imagepath != 'null':
        imagepath= 'static/'+imagepath
        if os.path.exists(imagepath):
            os.remove(imagepath)

def updateArtistImage(artist_image,artistid):
    deleteArtistImage(artistid)
    # Get the file extensions
    artist_image_extension = os.path.splitext(artist_image.filename)[1]
    # Specify the path where you want to save the uploaded files
    upload_folder = 'static/uploads/artist'  # Update the path according to your setup
    # Create the upload folder if it doesn't exist
    os.makedirs(upload_folder, exist_ok=True)
    # Customize the filenames
    artist_image_filename = str(artistid) + 'propic' + artist_image_extension
    # Saving the path for database
    profilepath='uploads/artist/' + str(artistid) + 'propic' + artist_image_extension
    # Save the uploaded files with the customized filenames
    artist_image.save(os.path.join(upload_folder, artist_image_filename))
    # Saving to database
    q="update artist set image_loc='%s' where artist_id='%s'"%(profilepath,artistid)
    update(q)

def deleteArtistImage(artistid):
    q="select image_loc from artist where artist_id='%s'"%(artistid)
    artistdetails=select(q)
    imagepath = artistdetails[0]['image_loc']
    if imagepath != 'null':
        imagepath= 'static/'+imagepath
        if os.path.exists(imagepath):
            os.remove(imagepath)

def updateArtistCover(artist_image,artistid):
    deleteArtistCover(artistid)
    # Get the file extensions
    artist_image_extension = os.path.splitext(artist_image.filename)[1]
    # Specify the path where you want to save the uploaded files
    upload_folder = 'static/uploads/artist'  # Update the path according to your setup
    # Create the upload folder if it doesn't exist
    os.makedirs(upload_folder, exist_ok=True)
    # Customize the filenames
    artist_image_filename = str(artistid) + 'cover' + artist_image_extension
    # Saving the path for database
    profilepath='uploads/artist/' + str(artistid) + 'cover' + artist_image_extension
    # Save the uploaded files with the customized filenames
    artist_image.save(os.path.join(upload_folder, artist_image_filename))
    # Saving to database
    q="update artist set cover_pic='%s' where artist_id='%s'"%(profilepath,artistid)
    update(q)

def deleteArtistCover(artistid):
    q="select cover_pic from artist where artist_id='%s'"%(artistid)
    artistdetails=select(q)
    imagepath = artistdetails[0]['cover_pic']
    if imagepath != 'null':
        imagepath= 'static/'+imagepath
        if os.path.exists(imagepath):
            os.remove(imagepath)