from playrecipe.repositories import MongoDBDAO, SpotifyAPI
import requests
import json
import logging
from datetime import datetime


class PlaylistDAO:

    def __init__(self, redirect_uri=None, request=None, code=None):
        self.db = MongoDBDAO().get_client().get_database('playrecipe')
        self.request = request
        self.code = code
        self.redirect_uri = redirect_uri

    def get_headers(self):
        refresh = False
        if "expire_time" in self.request.session:
            if (datetime.now() - datetime.strptime(self.request.session['expire_time'],
                                                   '%Y-%m-%d %H:%M:%S.%f')).seconds > 3600:
                code = self.request.session['refresh_token']
                refresh = True
            else:
                code = None
        else:
            code = self.code
        return SpotifyAPI(request=self.request).get_headers(self.redirect_uri, refresh, code)

    def get_collection(self, collection_name):
        return self.db.get_collection(collection_name)

    def upsert_playlists(self, username):
        headers = self.get_headers()
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"
        url = "https://api.spotify.com/v1/me/playlists"
        response = requests.get(url, headers=headers)
        playlists = json.loads(response.text)["items"]

        for playlist in playlists:
            del playlist["snapshot_id"]
            del playlist["type"]
            del playlist["uri"]
            del playlist["primary_color"]
            playlist["url"] = playlist["external_urls"]["spotify"]
            del playlist["external_urls"]
            del playlist["href"]
            playlist["image"] = playlist["images"][0]["url"]
            del playlist["images"]
            playlist["owner"] = playlist["owner"]["display_name"]
            tracks_url = playlist["tracks"]["href"]
            fields = "items(track(album(id,images(url),name,), artists(external_urls.spotify, id, name), external_urls.spotify, id,name,preview_url))"
            response = requests.get(tracks_url, params={"fields": fields}, headers=headers)
            tracks = json.loads(response.text)["items"]
            for i, track in enumerate(tracks):
                track["track"]["album"]["image"] = track["track"]["album"]["images"][0]["url"]
                del track["track"]["album"]["images"]
                tracks[i] = track["track"]
            playlist["tracks"] = tracks
        playlists = {"username": username, "playlists": playlists}
        collection = self.get_collection('playlists')
        try:
            collection.update_one({'username': username}, {'$set': playlists}, upsert=True)
            logging.info('upsert_playlists_success')
            return True
        except:
            logging.warning('upsert_playlists_error_occurs')
            return False

    def upsert_toptracks(self, username):
        headers = self.get_headers()
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"
        url = "https://api.spotify.com/v1/me/top/tracks"
        response = requests.get(url, headers=headers)
        toptracks = json.loads(response.text)['items']
        for toptrack in toptracks:
            del toptrack["album"]["available_markets"]
            del toptrack["album"]["artists"]
            del toptrack["album"]["uri"]
            del toptrack["album"]["type"]
            toptrack["image"] = toptrack["album"]["images"][0]["url"]
            del toptrack["album"]["images"]
            for artist in toptrack["artists"]:
                del artist["type"]
                del artist["uri"]
            del toptrack["available_markets"]
            del toptrack["disc_number"]
            del toptrack["external_ids"]
            del toptrack["external_urls"]
            del toptrack["href"]
            del toptrack["is_local"]
            del toptrack["type"]
            del toptrack["uri"]

        toptracks = {"username": username, "toptracks": toptracks}
        collections = self.get_collection("toptracks")
        try:
            collections.update_one({"username": username}, {"$set": toptracks}, upsert=True)
            logging.info('upsert_toptracks_success')
            return True
        except:
            logging.warning('upsert_toptracks_error_occurs')
            return False

    def upsert_topartists(self, username):
        headers = self.get_headers()
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"
        url = "https://api.spotify.com/v1/me/top/artists"
        response = requests.get(url, headers=headers)
        topartists = json.loads(response.text)['items']
        for topartist in topartists:
            del topartist["external_urls"]
            topartist["followers"] = topartist["followers"]["total"]
            del topartist["href"]
            topartist["image"] = topartist["images"][0]["url"]
            del topartist["images"]
            del topartist["uri"]
            del topartist["type"]
        topartists = {"username": username, "topartists": topartists}
        collections = self.get_collection("topartists")
        try:
            collections.update_one({"username": username}, {"$set": topartists}, upsert=True)
            logging.info('upsert_topartists_success')
            return True
        except:
            logging.warning('upsert_topartists_error_occurs')
            return False

    def read_playlists(self, username):
        collection = self.get_collection('playlists')
        projection = {}
        projection["_id"] = False
        projection["playlists.name"] = 1
        projection["playlists.owner"] = 1
        projection["playlists.image"] = 1
        projection["playlists.url"] = 1
        projection["playlists.tracks.album.image"] = 1
        projection["playlists.tracks.external_urls.spotify"] = 1
        projection["playlists.tracks.name"] = 1
        projection["playlists.tracks.artists.name"] = 1
        projection["playlists.tracks.artists.external_urls.spotify"] = 1
        projection["playlists.tracks.preview_url"] = 1
        return collection.find_one({"username": username}, projection=projection)

    def read_toptracks(self, username):
        collection = self.get_collection('toptracks')
        projection = {}
        projection["_id"] = False
        projection["toptracks.name"] = 1
        projection["toptracks.image"] = 1
        projection["toptracks.artists.name"] = 1
        projection["toptracks.popularity"] = 1
        projection["toptracks.preview_url"] = 1
        return collection.find_one({"username": username}, projection=projection)

    def read_topartists(self, username):
        collection = self.get_collection('topartists')
        projection = {}
        projection["_id"] = False
        projection["topartists.name"] = 1
        projection["topartists.image"] = 1
        projection["topartists.popularity"] = 1
        projection["topartists.genres"] = 1
        projection["topartists.followers"] = 1
        return collection.find_one({"username": username}, projection=projection)
