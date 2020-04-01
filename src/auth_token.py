import os

import spotipy
import spotipy.util as util

username = "terence"
scope = "user-library-read playlist-read-private playlist-modify-private"

token = util.prompt_for_user_token(username, scope,
                           client_id=os.environ['SPOTIPY_CLIENT_ID'],
                           client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
                           redirect_uri=os.environ['SPOTIPY_REDIRECT_URI'],
                           cache_path="cache/.cache-"+username)

sp = spotipy.Spotify(auth=token)