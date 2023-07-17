from database import *
import os
def songDeletion(sid):
    q="select * from songs where song_id='%s'"%(sid)
    songdetails=select(q)
    songdetails=songdetails[0]
    if len(songdetails) > 0:
        imagepath='static/'+songdetails['image_loc']
        songpath=songdetails['song_loc'][1:]
        if os.path.exists(imagepath):
            os.remove(imagepath)
        else:
            return("danger: Error Occured")
        if os.path.exists(songpath):
            os.remove(songpath)
        else:
            return("danger: Error Occured")
        q="delete from clicks where content_id='%s' and content_type='song'"%(sid)
        delete(q)
        q="delete from likes where content_id='%s' and content_type='song'"%(sid)
        delete(q)
        q="delete from playlisttrack where song_id='%s'"%(sid)
        delete(q)
        q="delete from songartist where song_id='%s'"%(sid)
        delete(q)
        q="delete from songs where song_id='%s'"%(sid)
        delete(q)
        return("warning: Song Successfully Deleted")
    else:
        return("danger: Song Not Available")
    
def artistSongRemoval(song_id):
    q="SELECT u.login_id FROM USER u INNER JOIN songs s ON s.user_id=u.user_id WHERE song_id='%s'"%(song_id)
    login_id=select(q)
    login_id=login_id[0]['login_id']
    q="insert into notification(user_id,content_id,content,content_status,status,notification_type) values('%s','%s','Song removed from artist','artistremoved','toread','songremoval')"%(login_id,song_id)
    insert(q)
    q="DELETE from songartist where song_id='%s'"%(song_id)
    delete(q)

def deleteArtist(artist_id):
    q="select * from artist where artist_id='%s'"%(artist_id)
    artistdata=select(q)
    artistdata=artistdata[0]
    if len(artistdata)>0:
        imagepath='static/'+artistdata['image_loc']
        coverpath='static/'+artistdata['cover_pic']
        if os.path.exists(imagepath):
            os.remove(imagepath)
        else:
            return("danger: Error Occured")
        if os.path.exists(coverpath):
            os.remove(coverpath)
        else:
            return("danger: Error Occured")
        q="select * from songartist where artist_id='%s'"%(artist_id)
        songartist=select(q)
        if len(songartist)>0:
            for song in songartist:
                artistSongRemoval(song['song_id'])
        q="delete from clicks where content_id='%s' and content_type='artist'"%(artist_id)
        delete(q)
        q="delete from likes where content_id='%s' and content_type='artist'"%(artist_id)
        delete(q)
        q="delete from artist where artist_id='%s'"%(artist_id)
        delete(q)
        return("warning: Artist Deleted successfully")
    else:
        return("danger: Artist Not Available")
    
def albumSongRemoval(song_id):
    q="SELECT u.login_id FROM USER u INNER JOIN songs s ON s.user_id=u.user_id WHERE song_id='%s'"%(song_id)
    login_id=select(q)
    login_id=login_id[0]['login_id']
    q="insert into notification(user_id,content_id,content,content_status,status,notification_type) values('%s','%s','Song removed from album','albumremoved','toread','songremoval')"%(login_id,song_id)
    insert(q)
    q="update songs set album_id='0' where song_id='%s'"%(song_id)
    update(q)

def deleteAlbum(album_id):
    q="select * from album where album_id='%s'"%(album_id)
    albumdata=select(q)
    albumdata=albumdata[0]
    if len(albumdata)>0:
        imagepath='static/'+albumdata['image_loc']
        coverpath='static/'+albumdata['cover_pic']
        if os.path.exists(imagepath):
            os.remove(imagepath)
        else:
            return("danger: Error Occured")
        if os.path.exists(coverpath):
            os.remove(coverpath)
        else:
            return("danger: Error Occured")
        q="select * from songs where album_id='%s'"
        albumsongs=select(q)
        if len(albumsongs)>0:
            for song in albumsongs:
                albumSongRemoval(song['song_id'])
        q="delete from clicks where content_id='%s' and content_type='album'"%(album_id)
        delete(q)
        q="delete from likes where content_id='%s' and content_type='album'"%(album_id)
        delete(q)
        q="delete from album where album_id='%s'"%(album_id)
        delete(q)
        return("warning: Album Deleted Successfully")
    else:
        return("danger: Album Not Available")