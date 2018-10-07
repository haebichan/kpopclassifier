import spotipy
import pandas as pd

from spotipy.oauth2 import SpotifyClientCredentials

my_id = '655e62800e724511b9a6f74b1bfa635f'
secret_key = '9e1f1feb45874771b24d1d10d19e87bd'


client_credentials_manager = SpotifyClientCredentials(client_id = my_id, client_secret = secret_key)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


redvelvet = 'https://open.spotify.com/artist/1z4g3DjTBBZKhvAroFlhOM'
twentyone = 'https://open.spotify.com/artist/1l0mKo96Jh9HVYONcRl3Yp'
ikon = 'https://open.spotify.com/artist/5qRSs6mvI17zrkJpOHkCoM'
superjunior = 'https://open.spotify.com/artist/5qRSs6mvI17zrkJpOHkCoM'
gfriend = 'https://open.spotify.com/artist/0qlWcS66ohOIi0M8JZwPft'
wannaone = 'https://open.spotify.com/artist/2CvaqAMMsX576VBehaJ0Wx'
bts = 'https://open.spotify.com/artist/3Nrfpe0tUJi4K4DXYWgMUX'
bigbang = 'https://open.spotify.com/artist/4Kxlr1PRlDKEB0ekOCyHgX'
gg = 'https://open.spotify.com/artist/0Sadg1vgvaPqGTOjxu0N6c'
exo = 'https://open.spotify.com/artist/3cjEqqelV9zb4BYE3qDQ4O'
twice = 'https://open.spotify.com/artist/7n2Ycct7Beij7Dj7meI4X0'
blackpink = 'https://open.spotify.com/artist/41MozSoPIsD1dJM0CLPjZF'
shinee = 'https://open.spotify.com/artist/2hRQKC0gqlZGPrmUKbcchR'

artist_list = [redvelvet, twentyone, ikon, superjunior, gfriend, wannaone, bts, bigbang, gg, exo, twice, blackpink,shinee]


feature_list = []

for artist in artist_list:
    
    artistalbums = sp.artist_albums(artist_id = artist, limit = 50)
    
    
    # go to their individual albums
    for i in range(len(artistalbums['items'])):
        album_uri = artistalbums['items'][i]['uri']
        album_tracks = sp.album_tracks(album_uri)
        
        #go to their individual tracks
        for j in range(len(album_tracks['items'])):
            album_song = album_tracks['items'][j]['uri']
            audiofeatures = sp.audio_features(album_song)
            
            #extract individual audio features of individual tracks
            for feature in audiofeatures:
                feature_list.append([feature['danceability'], feature['energy'], feature['key'], feature['speechiness'],
                                     feature['acousticness'], feature['instrumentalness'], feature['liveness'], feature['valence'],
                                     feature['tempo'], feature['duration_ms'],feature['time_signature'], artistalbums['items'][0]['artists'][0]['name']])


data = pd.DataFrame(feature_list, columns = ['danceability','energy','key','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','time_signature', 'artist_name'])

data.to_csv('extracted_song_features.csv')

