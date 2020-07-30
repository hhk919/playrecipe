from django.urls import path, re_path
from playlist.views import *

app_name = 'playlist'

urlpatterns = [
    # /playlist/
    path('', PlaylistView.as_view(), name='index'),
    # /playlist/callback/
    path('callback/', PlaylistCallbackView.as_view(), name='callback'),
    # /playlist/update/
    path('update/', PlaylistUpdate.as_view(), name='update'),
    # /playlist/toptracks/
    path('toptracks/',PlaylistTopTracks.as_view(), name='toptracks'),
    # /playlist/toptracks/callback/
    path('toptracks/callback/',ToptracksCallbackView.as_view(),name='toptrackcallback'),
    # /playlist/topartists/
    path('topartists/',PlaylistTopArtists.as_view(), name='topartists'),
    # /playlist/topartists/callback/
    path('topartists/callback/',TopartistsCallbackView.as_view(), name='topartistscallback'),

]
