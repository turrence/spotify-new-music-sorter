import config
import constant
import playlist
import saved_songs
import os
import threading
import time
import traceback
from datetime import datetime as dt
from datetime import timezone as tz
from web_auth import auth_server
from spotipy.oauth2 import SpotifyOAuth

import spotipy

class App(object):
    def __init__(self):
        if not os.path.exists(constant.CACHE_PATH):
            os.mkdir(constant.CACHE_PATH)
        self.update_clients()
    
    # Refreshes the access tokens and updates the playlists for all clients in 
    # the cache
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
            playlist.update_playlist(spotipy.Spotify(auth=token))

    def run_periodically(self):
        # update every 10 minutes
        threading.Timer(constant.UPDATE_FREQUENCY, self.run_periodically).start()
        print("Updating playlists....")
        try:
            self.update_clients()
        except Exception as e:
            with open(constant.SRC_PATH + '/../error.log', 'a') as f:
                f.write(str(e))
                f.write(traceback.format_exc())

app = App()
app.run_periodically()

# debug server
if __name__ == "__main__":
    # run the server in a background thread
    server_thread = threading.Thread(target = auth_server.run, kwargs=dict(port=config.port))
    server_thread.run()
