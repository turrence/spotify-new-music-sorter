import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, redirect, request
from client_manager import ClientManager

auth_server = Flask(__name__)
auth_server.debug = False

@auth_server.route('/')
def main():
    scope = "user-library-read playlist-read-private playlist-modify-private"
    oauth = SpotifyOAuth(
        scope=scope, 
        username="temp",
        # TODO: THIS SHOULD NOT BE OS.GETCWD
        cache_path=os.getcwd() + "/cache/.cache-temp"
    )
    # ask the user for authorization here
    if (len(request.args) == 0):
        return redirect(oauth.get_authorize_url())
    # we got the code here, use it to create a client
    else:
        print(request.args["code"])
        token = oauth.get_access_token(request.args["code"], as_dict=False)
        ClientManager.clients.append(spotipy.Spotify(auth=token))
        os.rename(os.getcwd() + "/cache/.cache-temp", os.getcwd() +
                  "/cache/.cache-" + ClientManager.clients[0].me()['id'])
        print(ClientManager.clients[0].me()['id'])
        return "Successfully authenticated, you may close this now"