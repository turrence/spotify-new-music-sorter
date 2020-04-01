import playlist
import saved_songs
from auth_token import sp

from datetime import datetime as dt
from datetime import timezone as tz

TARGET_PLAYLIST = playlist.get_target_playlist(dt.now(tz=tz.utc))
PLAYLIST_LAST_UPDATED = playlist.get_newest_date_in_playlist(TARGET_PLAYLIST)
SONGS_TO_BE_ADDED = saved_songs.get_unadded_songs(PLAYLIST_LAST_UPDATED)

if len(SONGS_TO_BE_ADDED) < 1:
    print("no songs to be added")
else:
    sp.user_playlist_add_tracks(sp.me()['id'], TARGET_PLAYLIST, SONGS_TO_BE_ADDED)
