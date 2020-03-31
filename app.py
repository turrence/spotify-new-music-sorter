import os
import spotipy
import spotipy.util as util

username = "terence"
scope = "playlist-modify-public"

token = util.prompt_for_user_token(username, scope,
                           client_id=os.environ['SPOTIPY_CLIENT_ID'],
                           client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
                           redirect_uri=os.environ['SPOTIPY_REDIRECT_URI'])
