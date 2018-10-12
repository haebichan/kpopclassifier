from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import enchant
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


my_id = '655e62800e724511b9a6f74b1bfa635f'
secret_key = '9e1f1feb45874771b24d1d10d19e87bd'

client_credentials_manager = SpotifyClientCredentials(client_id = my_id, client_secret = secret_key)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


dic = {'redvelvet':'red-velvet', 'twentyone':'2ne1', 'ikon': 'ikon', 'gfriend':'gfriend', 'wannaone':'wanna-one', 'bigbang':'big-bang', 'gg':'girls-generation','exo':'exo','twice':'twice','blackpink':'blackpink','shinee':'shinee', 'btob':'btob', 'aoa':'aoa', 'lovelyz':'lovelyz','seventeen':'seventeen'}


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

btob = 'https://open.spotify.com/artist/2hcsKca6hCfFMwwdbFvenJ'
aoa = 'https://open.spotify.com/artist/54gWVQFHf8IIqbjxAoOarN'
lovelyz = 'https://open.spotify.com/artist/3g34PW5oNmDBxMVUTzx2XK'
seventeen = 'https://open.spotify.com/artist/7nqOGRxlXj7N2JYbgNEjYH'


def create_and_store_lyrics(sp, artist_name = None, artist_dic = None):
    # this is for scraping genius.com

    dictionary = enchant.Dict("en_US")

    albums = sp.artist_albums(artist_id = artist_name, limit = 50)

    songs = []

    for i in range(len(albums['items'])):
        album_uri = albums['items'][i]['uri']
        album_tracks = sp.album_tracks(album_uri)

        for j in range(len(album_tracks['items'])):
            album_song = album_tracks['items'][j]['name']
            songs.append(album_song)


    global_list = []

    for title in songs:
        j = title.split()
        local_list = []
        for word in j:
            if word.isalnum() and dictionary.check(word) == True:
                local_list.append(word.lower())

        global_list.append('-'.join(local_list))

    res = []

    for i in range(len(global_list)):
        try:
            r = requests.get('https://genius.com/Genius-translations-' + dic[artist_dic] + '-' + global_list[i] + '-english-translation-lyrics')
            soup = BeautifulSoup(r.text, 'lxml')
            lyrics = soup.find('div', class_='lyrics').get_text()
            res.append([global_list[i], lyrics])
        except Exception as e:

            r = requests.get('https://genius.com/' + dic[artist_dic].title() + '-' + global_list[i] + '-lyrics')
            soup = BeautifulSoup(r.text, 'lxml')
            try:
                lyrics = soup.find('div', class_='lyrics').get_text()
                res.append([global_list[i], lyrics])
            except Exception as e:
                    pass


    df = pd.DataFrame(res).to_csv('lyrics_data/' + dic[artist_dic] + '_translated_lyrics.csv')


#
#def create_and_store_lyrics2(sp, artist_name = None, artist_dic = None):
#    # this is using kpopviral.com for webscraping
#
#    dictionary = enchant.Dict("en_US")
#
#    albums = sp.artist_albums(artist_id = artist_name, limit = 50)
#
#    songs = []
#
#    for i in range(len(albums['items'])):
#        album_uri = albums['items'][i]['uri']
#        album_tracks = sp.album_tracks(album_uri)
#
#        for j in range(len(album_tracks['items'])):
#            album_song = album_tracks['items'][j]['name']
#            songs.append(album_song)
#
#    global_list = []
#
#    for title in songs:
#        j = title.split()
#        local_list = []
#        for word in j:
#            if word.isalnum() and dictionary.check(word) == True:
#                local_list.append(word.lower())
#
#                global_list.append('-'.join(local_list))
#
#    res = []
#
#    for i in range(len(global_list)):
#        try:
#            r = requests.get('https://www.kpopviral.com/lyrics/' + dic[artist_dic] + '-' + global_list[i] + '-lyrics-english-romanized-translation.html')
#            soup = BeautifulSoup(r.text, 'lxml')
#            lyrics = soup.find('div', id = 'EnglishTranslation-0').get_text(strip = False)
#            res.append([global_list[i], lyrics])
#        except Exception as e:
#            pass
#
#
#
#    df = pd.DataFrame(res).to_csv('lyrics_data/' + dic[artist_dic] + '_translated_lyrics.csv')



create_and_store_lyrics(sp, artist_name = bigbang, artist_dic = 'bigbang')



























