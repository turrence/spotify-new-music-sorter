import config
import constant
import playlist
import saved_songs
import threading
import time
import os
from datetime import datetime as dt
from datetime import timezone as tz
from web_auth import auth_server
from spotipy.oauth2 import SpotifyOAuth

import spotipy

class App(object):
    def __init__(self):
        if not os.path.exists(constant.CACHE_PATH):
            os.mkdir(constant.CACHE_PATH)
        # load all clients: this only runs when we shut down the app and reboot it
        # alternative: solution when the app boots up, run the program
        self.update_clients()
    
    def update_clients(self):
        for filename in os.listdir(constant.CACHE_PATH):
            id = filename[len(".cache-"):]
            cache_path = constant.CACHE_PATH + "/.cache-" + id
            oauth = SpotifyOAuth(
                scope = constant.SCOPE,
                username = id,
                cache_path = cache_path,
                client_id = config.client_id,
                client_secret = config.client_secret,
                redirect_uri = config.redirect_uri
            )
            token = oauth.get_cached_token()['access_token']
            self.update_playlist(spotipy.Spotify(auth = token))

    def update_playlist(self, sp):
        target_playlist = playlist.get_target_playlist(dt.now(tz=tz.utc), sp)
        # in utc
        last_updated = playlist.get_newest_date_in_playlist(target_playlist, sp)
        songs_to_be_added = saved_songs.get_unadded_songs(last_updated, sp)
        if len(songs_to_be_added) < 1:
            print("no songs to be added for", sp.me()['id'])
        else:
            sp.user_playlist_add_tracks(sp.me()['id'], target_playlist, songs_to_be_added)

    def run_periodically(self):
        # update every 10 minutes
        threading.Timer(constant.UPDATE_FREQUENCY, self.run_periodically).start()
        print("Updating playlists....")
        self.update_clients()

if __name__ == "__main__":
    app = App()
    app.run_periodically()
    # run the server in a background thread
    server_thread = threading.Thread(target = auth_server.run, kwargs=dict(port=config.port))
    server_thread.run() 