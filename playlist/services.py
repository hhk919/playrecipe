from playrecipe.repositories import SpotifyAPI
from playlist.repositories import PlaylistDAO


def get_auth(redirect_uri=None, scope=None):
    return SpotifyAPI().get_auth(redirect_uri, scope)


def upsert_playlists(redirect_uri, request, username, code=None):
    return PlaylistDAO(redirect_uri, request, code).upsert_playlists(username)


def get_lists(username):
    return PlaylistDAO().read_playlists(username)


def upsert_toptracks(redirect_uri, request, username, code=None):
    return PlaylistDAO(redirect_uri, request, code).upsert_toptracks(username)


def get_toptracks(username):
    return PlaylistDAO().read_toptracks(username)


def upsert_topartists(redirect_uri, request, username, code=None):
    return PlaylistDAO(redirect_uri, request, code).upsert_topartists(username)


def get_topartists(username):
    return PlaylistDAO().read_topartists(username)
