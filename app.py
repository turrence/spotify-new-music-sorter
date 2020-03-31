import os
import pprint
import spotipy
import spotipy.util as util

username = "terence"
scope = "user-library-read playlist-modify-public"

token = util.prompt_for_user_token(username, scope,
                           client_id=os.environ['SPOTIPY_CLIENT_ID'],
                           client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
                           redirect_uri=os.environ['SPOTIPY_REDIRECT_URI'])
'''
get users "saved tracks" ===? Liked Songs
add to selected playlist
'''

sp = spotipy.Spotify(auth=token)

songs = sp.current_user_saved_tracks(2)

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(songs)

