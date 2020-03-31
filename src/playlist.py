from datetime import datetime as dt
from auth_token import sp

import constant
import pprint

pp = pprint.PrettyPrinter(indent=2)

# returns the season given a time
def get_current_season(now) -> str:
    if now.month > 2 and now.month < 6: # MAR - MAY
        return constant.SPRING
    elif now.month > 5 and now.month < 9: # JUN - AUG
        return constant.SUMMER
    elif now.month > 8 and now.month < 12: # SEPT - NOV
        return constant.FALL
    else: # DEC - FEB
        return constant.WINTER     

# returns the playlist id based on date
def get_target_playlist(date) -> str:
    # TODO: current_user vs other users
    target_playlist_name = get_current_season(date)+ " " + str(date.year)
    # TODO: assume playlist is within first 50 for rn, offset arg in sp.current_user_playlist
    all_playlists = {playlist['name']: playlist['id'] for playlist in sp.current_user_playlists(50)['items']}
    if all_playlists[target_playlist_name] is None:
        # TODO: create playlist
        # sp.user_playlist_create(user, name, public=True, description='')
        print("creating the playlist", target_playlist_name)
    else:
        return all_playlists[target_playlist_name]

# returns a datetime object of the most recently added song of a playlist
def get_newest_date_in_playlist(pl_id):
    # assume chronologically added ordered playlist
    songs = sp.playlist_tracks(pl_id, fields="items, total")
    if songs['total'] == 0:
        return None
    # in utc
    return dt.strptime(songs['items'][songs['total'] - 1]['added_at'], "%Y-%m-%dT%H:%M:%SZ") 

