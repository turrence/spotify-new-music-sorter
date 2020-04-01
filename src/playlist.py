from datetime import datetime as dt
from auth_token import sp, username

import constant

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
    # december of 2019 creates playlist "winter 2020"
    target_playlist_name = get_current_season(date)+ " " + str(date.year if date.month != 12 else date.year+1)
    chunk, offset = 50, 0
    all_playlists = {}
    """
    ASSUMPTIONS: a user has no duplicate playlist names

    in the case that a user has a duplicate playlist name, the script will modify
    the one 'lower' in the user's playlist library
    """
    while True: 
        playlist_info = sp.current_user_playlists(chunk, offset)
        for item in playlist_info['items']:
            all_playlists[item['name']] = item['id']
        if len(all_playlists) >= playlist_info['total']:
            break
        else:
            offset += chunk

    if all_playlists[target_playlist_name] is None:
        resp = sp.user_playlist_create(sp.me()['id'], target_playlist_name, public=False, 
            description='AUTOMATED PLAYLIST - MODIFYING THIS PLAYLIST MAY RESULT IN UNEXPECTED BEHAVIORS \
                (you can change the description tho)')
        return resp['id']
    else:
        return all_playlists[target_playlist_name]

# returns a datetime object of the most recently added song of a playlist
def get_newest_date_in_playlist(pl_id):
    # assume chronologically added ordered playlist
    songs = sp.playlist_tracks(pl_id, fields="items, total")
    if songs['total'] == 0: # what if its an empty playlist
        return None  
    # in utc
    return dt.strptime(songs['items'][songs['total'] - 1]['added_at'], "%Y-%m-%dT%H:%M:%SZ") 

