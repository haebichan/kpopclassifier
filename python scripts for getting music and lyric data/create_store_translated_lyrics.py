from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import enchant
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from builtins import any as b_any

my_id = 'insert yours here'
secret_key = 'insert yours here'

client_credentials_manager = SpotifyClientCredentials(client_id = my_id, client_secret = secret_key)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


dic = {'redvelvet':'red-velvet', 'twentyone':'2ne1', 'ikon': 'ikon', 'gfriend':'gfriend', 'wannaone':'wanna-one', 'bigbang':'big-bang', 'gg':'girls-generation','exo':'exo','twice':'twice','blackpink':'blackpink','shinee':'shinee', 'btob':'btob', 'aoa':'aoa', 'lovelyz':'lovelyz','seventeen':'seventeen', 'bts':'BTS'}


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
            if [global_list[i], lyrics] not in res:
                res.append([global_list[i], lyrics])
        except Exception as e:

            r = requests.get('https://genius.com/' + dic[artist_dic].title() + '-' + global_list[i] + '-lyrics')
            soup = BeautifulSoup(r.text, 'lxml')
            try:
                lyrics = soup.find('div', class_='lyrics').get_text()
                if 'English Translation' in lyrics:
                    
                    lyrics_split = lyrics.split('English Translation')

                    search_list = ['Japanese Translation','Romanized','Korean Original','Hangul','French Translation','Romanization', 'Chinese Translation','Original','Chinese','Japanese','French','Korean']

                    s = lyrics.split('English Translation')[1].split()

                    for index in range(len(s)):
                        next_index = index + 1
                        if b_any(substring in lyrics for substring in search_list):
                            while s[next_index] not in search_list and next_index < len(s) -1:
                                next_index +=1
                            
                            english_lyrics = ' '.join(s[index:next_index])
                            break

                        else:
                            english_lyrics = ' '.join(s)

                    if [global_list[i], english_lyrics] not in res:
                        res.append([global_list[i], english_lyrics])

        
            except Exception as e:
                    pass


    df = pd.DataFrame(res).to_csv('lyrics_data/' + dic[artist_dic] + '_translated_lyrics.csv')




create_and_store_lyrics(sp, artist_name = bts, artist_dic = 'bts')



























