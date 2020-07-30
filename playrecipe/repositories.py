from pymongo import MongoClient
from static.file import spotify_api_client
import base64
import requests
import json
from urllib.parse import urlencode
from datetime import datetime


class MongoDBDAO:

    def __init__(self):
        self.client = MongoClient()

    def get_client(self):
        return self.client


class SpotifyAPI:

    def __init__(self, request=None):
        self.client_id = spotify_api_client.Client_ID
        self.client_secret = spotify_api_client.Client_Secret
        self.request = request

    def get_auth(self, redirect_uri=None, scope=None):
        endpoint = 'https://accounts.spotify.com/authorize'
        scope = scope
        payload = {'client_id': self.client_id, 'response_type': 'code', 'redirect_uri': redirect_uri,
                   'scope': scope, 'show_dialog': True}
        # payload = {'client_id': self.client_id, 'response_type': 'code', 'redirect_uri': redirect_uri,
        #            'scope': scope}
        return endpoint + '?' + urlencode(payload)

    def get_headers(self, redirect_uri, refresh, code=None):
        if code:
            endpoint = 'https://accounts.spotify.com/api/token'
            authorization = base64.b64encode('{}:{}'.format(self.client_id, self.client_secret).encode('utf-8')).decode(
                'utf-8')
            token_headers = {"Authorization": "Basic {}".format(authorization)}
            if refresh:
                payload = {"grant_type": "refresh_token", "refresh_token": code, "redirect_uri": redirect_uri}
            else:
                payload = {"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri}
            response = requests.post(endpoint, data=payload, headers=token_headers)
            contents = json.loads(response.text)
            access_token = contents["access_token"]
            self.request.session['expire_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            if not refresh:
                self.request.session['refresh_token'] = contents["refresh_token"]
            self.request.session['access_token'] = access_token
        else:
            access_token = self.request.session['access_token']
        headers = {'Authorization': 'Bearer {}'.format(access_token)}
        return headers
