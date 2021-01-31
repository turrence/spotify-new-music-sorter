import config
import constant
import database
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError
from flask import Flask, redirect, request, render_template
from playlist import update_playlist

auth_server = Flask(__name__)
auth_server.debug = False

@auth_server.route('/')
def frontpage():
    return render_template("index.html", url=config.redirect_uri)

@auth_server.route('/login')
def auth_page():
    oauth = SpotifyOAuth(
        scope = constant.SCOPE, 
        username = "temp",
        cache_path = constant.CACHE_PATH + "/.cache-temp",
        client_id = config.client_id,
        client_secret = config.client_secret,
        redirect_uri = config.redirect_uri + "/login"
    )
    # ask the user for authorization here
    if ("code" not in request.args):
        # remove the temp file in case auth was not successful
        try:
            os.remove(oauth.cache_path)
        except OSError:
            pass
        return redirect(oauth.get_authorize_url())
    else:
        # TODO: backend logic probably doesn't belong here
        # we got the code here, use it to create a token
        print("Response Code: " + request.args["code"])
        try:
            token = oauth.get_access_token(request.args["code"], as_dict=False)
        except SpotifyOauthError:
            # remove the temp file in case auth was not successful
            try:
                os.remove(oauth.cache_path)
            except OSError:
                pass
            return render_template("auth_fail.html", url=config.redirect_uri)
        # which we use to create a client
        client = spotipy.Spotify(auth=token)
        client_cache = constant.CACHE_PATH + "/.cache-" + client.me()['id']
        
        # create a new playlist for new users
        if not os.path.exists(client_cache):
            update_playlist(client)
        
        # rename cache file to user
        os.rename(oauth.cache_path, client_cache)
        
        # add user to database
        database.add_user(client.me()['id'])

        return render_template("auth_success.html")

@auth_server.route('/logout')
def logout_page():
    oauth = SpotifyOAuth(
        scope=constant.SCOPE,
        username="temp",
        cache_path=constant.CACHE_PATH + "/.cache-temp",
        client_id=config.client_id,
        client_secret=config.client_secret,
        redirect_uri=config.redirect_uri + "/logout"
    )
    # get another authorization code so we know who we're logging out
    if ("code" not in request.args):
        return redirect(oauth.get_authorize_url())
    else:
        logout_page = render_template("logout_sucess.html")
        print("Response Code: " + request.args["code"])
        try:
            token = oauth.get_access_token(request.args["code"], as_dict=False)
        except SpotifyOauthError:
            return render_template("logout_fail.html")
        # which we use to create a client
        client = spotipy.Spotify(auth=token)
        # this is apparently the pythonic way to do this
        try:
            os.remove(constant.CACHE_PATH + "/.cache-" + client.me()['id'])
        except OSError:
            logout_page = render_template("logout_fail.html", id=client.me()['id'])
        try:
            os.remove(oauth.cache_path)
        except OSError:
            pass
        return logout_page

@auth_server.route('/check_status')
def status_check():
    return "work in progress, come back later!"
