import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, redirect, request

from playlist import get_newest_date_in_playlist

app = Flask(__name__)
clients = []


@app.route('/')
def main():
    scope = "user-library-read playlist-read-private playlist-modify-private"
    oauth = SpotifyOAuth(scope=scope, username="temp")
    # ask the user for authorization here
    if (len(request.args) == 0):
        return redirect(oauth.get_authorize_url())
    # we got the code here, use it to create a client
    else:
        print(request.args["code"])
        token = oauth.get_access_token(request.args["code"], as_dict=False)
        clients.append(spotipy.Spotify(auth=token))
        print(get_newest_date_in_playlist(
            "1VjQ8zUVT6nCx6HKkctISE", clients[0]))
        return "Successfully authenticated, you may close this now"


if __name__ == '__main__':
    app.run()