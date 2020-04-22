import config
import constant
import playlist
import saved_songs
import os
import spotipy
import sys
import threading
import time
import traceback
from datetime import datetime as dt
from datetime import timezone as tz
from spotipy.oauth2 import SpotifyOAuth

class App(object):
    def __init__(self):
        if not os.path.exists(constant.CACHE_PATH):
            os.mkdir(constant.CACHE_PATH)
    
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
            try:
                playlist.update_playlist(spotipy.Spotify(auth=token))
            except Exception as e:
                message = "Unable to update playlist for: " + id + "\n"
                message += str(e)
                print(message)
                with open(constant.SRC_PATH + '/../error.log', 'a') as f:
                    f.write(message)
                    f.write(traceback.format_exc())

    # Runs every n seconds on a separate thread
    # update_frequency: how frequently to update in seconds
    def run(self, update_frequency):
        threading.Timer(update_frequency, self.run, kwargs=dict(
            update_frequency=update_frequency)).start()
        print("Updating playlists....")
        try:
            self.update_clients()
        except Exception as e:
            with open(constant.SRC_PATH + '/../error.log', 'a') as f:
                f.write(str(e))
                f.write(traceback.format_exc())


if __name__ == "__main__":
    debug = False
    if len(sys.argv) >= 2:
        if sys.argv[1] == "--debug":
            debug = True
    app = App()
    # update faster if we're using the debug environment
    app.run(10 if debug else constant.UPDATE_FREQUENCY)

    # debug server
    if debug:
        from web_auth import auth_server
        # run the server in a background thread
        server_thread = threading.Thread(target = auth_server.run, kwargs=dict(port=config.port))
        server_thread.run()