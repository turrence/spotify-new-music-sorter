import os
import pprint
import spotipy
import spotipy.util as util

username = "terence"
scope = "user-library-read playlist-modify-public playlist-read-private"

token = util.prompt_for_user_token(username, scope,
                           client_id=os.environ['SPOTIPY_CLIENT_ID'],
                           client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
                           redirect_uri=os.environ['SPOTIPY_REDIRECT_URI'])
'''
get users "saved tracks" ===? Liked Songs
add to selected playlist
'''

sp = spotipy.Spotify(auth=token)


# gets liked songs
songs_liked = sp.current_user_saved_tracks(2) # need to determine how many songs to get
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(type(songs_liked['items'][0]['added_at']))
# date-added format: 2020-03-30T02:38:11Z
# -----------------: yyyy-dd-mmThh:mm:ss(TZD)
# TZD is TimeZoneDesignator: Z means UTC


# find playlist to add
playlist = sp.current_user_playlists(3)
for play in playlist['items']:
    # print(play['name'])
    break

# gets liked songs
songs_liked = sp.current_user_saved_tracks(2) # need to determine how many songs to get
pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(songs_liked)


# which playlist do i add to



