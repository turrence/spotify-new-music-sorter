import config
import constant
import playlist
import saved_songs
import threading
import time
import os
from client_manager import ClientManager
from datetime import datetime as dt
from datetime import timezone as tz
from web_auth import auth_server


class App(object):
    def __init__(self):
        if not os.path.exists(constant.CACHE_PATH):
            os.mkdir(constant.CACHE_PATH)
        self.clients = ClientManager()
        # load all clients
        self.clients.load_clients_from_cache()

    def update_playlists(self):
        for c in ClientManager.clients:
            target_playlist = playlist.get_target_playlist(dt.now(tz=tz.utc), c)
            # in utc
            last_updated = playlist.get_newest_date_in_playlist(target_playlist, c)
            songs_to_be_added = saved_songs.get_unadded_songs(last_updated, c)
            if len(songs_to_be_added) < 1:
                print("no songs to be added for", c.me()['id'])
            else:
                c.user_playlist_add_tracks(c.me()['id'], target_playlist, songs_to_be_added)

    def run_periodically(self):
        # update every 10 minutes
        threading.Timer(constant.UPDATE_FREQUENCY, self.run_periodically).start()
        self.clients.refresh_clients()
        self.update_playlists()
        

if __name__ == "__main__":
    app = App()
    app.run_periodically()
    # run the server in a background thread
    server_thread = threading.Thread(target = auth_server.run, kwargs=dict(port=config.port))
    server_thread.run()