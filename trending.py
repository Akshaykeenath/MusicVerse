from database import *
def get_album_data():
    album_data = []
    q = "select * from album"
    albums = select(q)
    for album in albums:
        album_id = album['album_id']
        q="select * from songs where privacy='public' and status='approved' and album_id='%s'"%(album_id)
        song_data=select(q)
        if song_data == []:
            continue
        q = "select count(*) as clicks from clicks where content_id='%s' and content_type='album'" % (album_id)
        clicks_count = select(q)
        q = "select count(*) as likes from likes where content_id='%s' and content_type='album'" % (album_id)
        likes_count = select(q)
        likes = int(likes_count[0]['likes']) * 2
        clicks = int(clicks_count[0]['clicks'])
        score = str(likes + clicks)
        album_data.append({
            'album_id': album['album_id'],
            'album_name': album['album_name'],
            'image_loc': album['image_loc'],
            'cover_pic': album['cover_pic'],
            'user_id': album['user_id'],
            'likes': likes_count[0]['likes'],
            'clicks': clicks_count[0]['clicks'],
            'score': score
        })

    sorted_albumdata = sorted(album_data, key=lambda x: int(x['score']), reverse=True)
    top_5_albums = sorted_albumdata[:5]
    return top_5_albums

# Gets Top 5 artists with artist id, name,likes,clicks,cover pic and artist pics as artist_cover_pic and artist_image_loc
def get_artist_data():
    artist_data = []
    q = "select * from artist"
    artists = select(q)
    for artist in artists:
        artist_id = artist['artist_id']
        q="SELECT * FROM songartist INNER JOIN songs USING (song_id) WHERE artist_id='%s' AND privacy='public' AND STATUS='approved'"%(artist_id)
        song_data=select(q)
        if song_data == []:
            continue
        q = "select count(*) as clicks from clicks where content_id='%s' and content_type='artist'" % (artist_id)
        clicks_count = select(q)
        q = "select count(*) as likes from likes where content_id='%s' and content_type='artist'" % (artist_id)
        likes_count = select(q)
        likes = int(likes_count[0]['likes']) * 2
        clicks = int(clicks_count[0]['clicks'])
        score = str(likes + clicks)
        artist_data.append({
            'artist_id': artist['artist_id'],
            'artist_name': artist['artist_name'],
            'artist_image_loc': artist['image_loc'],
            'artist_cover_pic': artist['cover_pic'],
            'user_id': artist['user_id'],
            'likes': likes_count[0]['likes'],
            'clicks': clicks_count[0]['clicks'],
            'score': score
        })

    sorted_artistdata = sorted(artist_data, key=lambda x: int(x['score']), reverse=True)
    top_5_artists = sorted_artistdata[:5]
    return top_5_artists


#Top 10 songs with all the song details and likes, clicks, liked(yes or no), score
def get_song_data(uid):
    song_data = []
    q = "select * from songs where status='approved' and privacy='public'"
    songs = select(q)
    for song in songs:
        song_id = song['song_id']
        q="select * from songartist where song_id='%s'"%(song_id)
        artist_data=select(q)
        if artist_data == []:
            continue
        if song['album_id'] == '0':
            continue
        q = "select count(*) as clicks from clicks where content_id='%s' and content_type='song'" % (song_id)
        clicks_count = select(q)
        q = "select count(*) as likes from likes where content_id='%s' and content_type='song'" % (song_id)
        likes_count = select(q)
        likes = int(likes_count[0]['likes']) * 2
        clicks = int(clicks_count[0]['clicks'])
        score = str(likes + clicks)
        q="select * from likes where content_id='%s' and user_id='%s' and content_type='song'"%(song_id,uid)
        check_like=select(q)
        album_id=song['album_id']
        q="select album_name from album where album_id='%s'"%(album_id)
        album_data=select(q)
        album_name=album_data[0]['album_name']
        if check_like == []:
            liked='no'
        else:
            liked='yes'
        song_data.append({
            'song_id': song['song_id'],
            'song_name': song['song_name'],
            'album_name': album_name,
            'song_image_loc': song['image_loc'],
            'song_loc': song['song_loc'],
            'genre': song['genre'],
            'date': song['date'],
            'language': song['language'],
            'user_id': song['user_id'],
            'privacy': song['privacy'],
            'duration': song['duration'],
            'status': song['status'],
            'liked': liked,
            'likes': likes_count[0]['likes'],
            'clicks': clicks_count[0]['clicks'],
            'score': score
        })

    sorted_songdata = sorted(song_data, key=lambda x: int(x['score']), reverse=True)
    top_5_songs = sorted_songdata[:5]
    return top_5_songs