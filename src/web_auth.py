import config
import constant
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, redirect, request, render_template
from playlist import update_playlist

auth_server = Flask(__name__)
auth_server.debug = False

@auth_server.route('/')
def auth_page():
    oauth = SpotifyOAuth(
        scope = constant.SCOPE, 
        username = "temp",
        cache_path = constant.CACHE_PATH + "/.cache-temp",
        client_id = config.client_id,
        client_secret = config.client_secret,
        redirect_uri = config.redirect_uri
    )
    # ask the user for authorization here
    if ("code" not in request.args):
        return redirect(oauth.get_authorize_url())
    else:
        # TODO: backend logic probably doesn't belong here
        # we got the code here, use it to create a token
        print("Response Code: " + request.args["code"])
        token = oauth.get_access_token(request.args["code"], as_dict=False)
        # which we use to create a client
        client = spotipy.Spotify(auth=token)
        client_cache = constant.CACHE_PATH + "/.cache-" + client.me()['id']
        # create a new playlist for new users
        if not os.path.exists(client_cache):
            update_playlist(client)
        os.rename(oauth.cache_path, client_cache)
        return "Successfully authenticated, you may close this now"

@auth_server.route('/logout')
def logout_page():
    return
