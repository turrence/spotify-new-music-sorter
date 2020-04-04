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

<<<<<<< HEAD
    def update_playlists(self):
        for c in ClientManager.clients:
            target_playlist = playlist.get_target_playlist(dt.now(tz=tz.utc), c)
            # in utc
            last_updated = playlist.get_newest_date_in_playlist(target_playlist, c)
            songs_to_be_added = saved_songs.get_unadded_songs(last_updated, c)
            if len(songs_to_be_added) >= 1:
                c.user_playlist_add_tracks(c.me()['id'], target_playlist, songs_to_be_added)
=======
    def update_playlist(self, sp):
        target_playlist = playlist.get_target_playlist(dt.now(tz=tz.utc), sp)
        # in utc
        last_updated = playlist.get_newest_date_in_playlist(target_playlist, sp)
        songs_to_be_added = saved_songs.get_unadded_songs(last_updated, sp)
        if len(songs_to_be_added) < 1:
            print("no songs to be added for", sp.me()['id'])
        else:
            sp.user_playlist_add_tracks(sp.me()['id'], target_playlist, songs_to_be_added)
>>>>>>> daae0f884059e1340da922013f53d840143c8a27

    def run_periodically(self):
        # update every 10 minutes
        threading.Timer(constant.UPDATE_FREQUENCY, self.run_periodically).start()
<<<<<<< HEAD
        try:
            self.clients.refresh_clients()
            self.update_playlists()
        except Exception as e:
            with open(constant.SRC_PATH + '/../error.log', 'a') as f:
                f.write(str(e))
                f.write(traceback.format_exc())

app = App()
app.run_periodically()
=======
        print("Updating playlists....")
        self.update_clients()

if __name__ == "__main__":
    app = App()
    app.run_periodically()
    # run the server in a background thread
    server_thread = threading.Thread(target = auth_server.run, kwargs=dict(port=config.port))
    server_thread.run() 
>>>>>>> daae0f884059e1340da922013f53d840143c8a27
