import spotipy
from spotipy.oauth2 import SpotifyOAuth

import spotipy
import spotipy.util as util

def get_spotify_token():
    username = '咕谷酱'
    scope = 'user-read-playback-state'
    gettokne = util.prompt_for_user_token(username,scope,
                            client_id='xxxx',
                            client_secret='xxxx',
                            # 注意需要在自己的web app中添加redirect url
                            redirect_uri='https://gmoe.cc')
    return gettokne

get_spotify_token()