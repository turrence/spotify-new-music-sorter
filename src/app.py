import config
import constant
import database
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
        database.init_database()

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
            try:
                token = oauth.get_cached_token()['access_token']
                playlist.update_playlist(spotipy.Spotify(auth=token))
            except Exception as e:
                timestamp = dt.now(tz=tz.utc).strftime('%Y-%m-%d %H:%M:%S')
                # message = "Unable to update playlist for: " + id + "\n"
                message = str(e)
                message = timestamp + ": " + message
                # print(message)
                database.increment_field(id, "error_count")
                database.update_user(id, "last_error", message)
                # with open(constant.SRC_PATH + '/../error.log', 'a') as f:
                #     f.write(message)
                #     f.write(traceback.format_exc())

                # if a user passes a certain number of errors, delete their 
                # token, they probably revoked our access
                if database.get_field(id, "error_count") > constant.ERROR_THRESHOLD:
                    try:
                        os.remove(filename)
                    except OSError:
                        pass
                    database.remove_user(id)


    # Runs every n seconds on a separate thread
    # update_frequency: how frequently to update in seconds
    def run(self, update_frequency):
        threading.Timer(update_frequency, self.run, kwargs=dict(
            update_frequency=update_frequency)).start()
        timestamp = dt.now(tz=tz.utc).strftime('%Y-%m-%d %H:%M:%S')
        # print(timestamp + ": Updating playlists....")
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