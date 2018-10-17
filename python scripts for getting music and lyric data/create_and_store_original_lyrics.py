from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import enchant
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from builtins import any as b_any

my_id = '655e62800e724511b9a6f74b1bfa635f'
secret_key = '9e1f1feb45874771b24d1d10d19e87bd'

client_credentials_manager = SpotifyClientCredentials(client_id = my_id, client_secret = secret_key)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


dic = {'bts':'Bts','redvelvet':'red-velvet', 'twentyone':'2nse1', 'ikon': 'ikon', 'gfriend':'gfriend', 'wannaone':'wanna-one', 'bigbang':'big-bang', 'gg':'girls-generation','exo':'exo','twice':'twice','blackpink':'blackpink','shinee':'shinee', 'btob':'btob', 'aoa':'aoa', 'lovelyz':'lovelyz','seventeen':'seventeen'}


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
            r = requests.get('https://genius.com/' + dic[artist_dic] + '-' + global_list[i] + '-lyrics')
            soup = BeautifulSoup(r.text, 'lxml')
            lyrics = soup.find('div', class_='lyrics').get_text().lower()


            split_list = ['hangul','korean','korean original']
            
            search_list = ['japanese','romanized','french','romanization', 'original','chinese','japanese','english','translation']
            
            total_list = split_list + search_list


            if not b_any(substring in lyrics for substring in total_list): # 1) if this is just pure Korean text. Sometimes there will be translated lyrics without explicit mention of translations, resulting in these lyrics being stored. 
                if [global_list[i], lyrics] not in res:
                    res.append([global_list[i], lyrics]) # just append the Korean text 

            else:
                if any(substring in lyrics for substring in split_list): # 2) if this has Korean lyrics mixed with other translations:
                    split_string = [i for i in filter(lambda x: x in lyrics, split_list)][0]

                    s = lyrics.split(split_string)[1].split()
                    for index in range(len(s)):
                        next_index = index + 1
                                
                        if b_any(substring in lyrics for substring in search_list):
                            while s[next_index] not in search_list and next_index < len(s) -1:
                                next_index +=1
                                            
                            korean_lyrics = ' '.join(s[index:next_index]) # use sliding window to find the end of korean lyrics through key words in search_list and extract the korean lyrics
                            break


                    if [global_list[i], korean_lyrics] not in res: # append the found Korean lyrics to the result list
                        res.append([global_list[i], korean_lyrics])



                else:  # 3) if these are foreign translations without Korean words, just drop it
                    pass
                                
                    

        except Exception as e: # if the link itself doesn't work, just drop the song
            pass


        
    df = pd.DataFrame(res).to_csv('../lyrics_data/Korean_lyrics/' + dic[artist_dic] + '_original_lyrics.csv')


create_and_store_lyrics(sp, artist_name = exo, artist_dic = 'exo')



























