import constant
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class ClientManager():
    clients = []

    def refresh_clients(self):
        for i in range(len(ClientManager.clients)):
            id = ClientManager.clients[i].me()['id']
            cache_path = constant.CACHE_PATH + "/.cache-" + \
                ClientManager.clients[i].me()['id']
            f = open(cache_path)
            token = json.loads(f.read())
            f.close()
            oauth = SpotifyOAuth(
                scope = constant.SCOPE,
                username = id,
                cache_path = cache_path
            )
            token = oauth.refresh_access_token(token["refresh_token"])
            ClientManager.clients[i] = spotipy.Spotify(auth = token)
    def load_clients_from_cache(self):
        for filename in os.listdir(constant.CACHE_PATH):
            f = open(constant.CACHE_PATH + "/" + filename)
            token = json.loads(f.read())
            f.close()
            id = filename[len(".cache-"):]
            cache_path = constant.CACHE_PATH + "/.cache-" + id
            oauth = SpotifyOAuth(
                scope = constant.SCOPE,
                username = id,
                cache_path = cache_path
            )
            token = oauth.refresh_access_token(token["refresh_token"])
            ClientManager.clients.append(spotipy.Spotify(auth = token))
