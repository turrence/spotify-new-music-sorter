import playlist
import saved_songs
import threading
import time
from client_manager import ClientManager
from datetime import datetime as dt
from datetime import timezone as tz
from web_auth import auth_server


class App(object):
    def __init__(self):
        # load all clients
        pass

    def update_all(self):
        for c in ClientManager.clients:
            target_playlist = playlist.get_target_playlist(dt.now(tz=tz.utc), c)
            # in utc
            last_updated = playlist.get_newest_date_in_playlist(target_playlist, c)
        songs_to_be_added = saved_songs.get_unadded_songs(last_updated, c)
        if len(songs_to_be_added) < 1:
            print("no songs to be added")
        else:
            c.user_playlist_add_tracks(c.me()['id'], target_playlist, songs_to_be_added)
    def run_periodically(self):
        threading.Timer(10, self.run_periodically).start()
        # print("hi")
        

if __name__ == "__main__":
    app = App()
    app.run_periodically()
    # run the server in a backtround thread
    server_thread = threading.Thread(target = auth_server.run, args=())
    server_thread.run()
