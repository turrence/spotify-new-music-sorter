from collections import deque
from datetime import timezone as tz
from datetime import datetime as dt

# returns a list of song ids
def get_unadded_songs(dt_threshold, client) -> deque:
    """
    finds all songs that were added past the last date
    """
    song_ids = deque()
    chunks, offset = 20, 0
    while True:
        songs_liked = client.current_user_saved_tracks(chunks, offset)
        for song in songs_liked['items']:
            if dt_threshold < dt.strptime(song['added_at'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=tz.utc):
                song_ids.append(song['track']['id'])
            else: 
                return song_ids
        # edge case: user has less liked songs than the chunk size
        if len(songs_liked['items']) < chunks:
            return song_ids
        offset += chunks