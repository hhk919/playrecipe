# Create your views here.
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render
from playlist.services import *
from django.utils.http import unquote
from django.contrib import messages


class PlaylistCallbackView(RedirectView):
    permanent = True
    pattern_name = 'playlist:index'

    def get_redirect_url(self, *args, **kwargs):
        if 'access_token' not in self.request.session :
            code = self.request.GET.get('code', None)
            result = upsert_playlists('http://localhost:8000/playlist/callback/', self.request, str(self.request.user), code)
        else:
            result = upsert_playlists('http://localhost:8000/playlist/callback/', self.request, str(self.request.user))

        if result:
            messages.success(self.request, 'Update Successfully~')
            return super().get_redirect_url(*args, **kwargs)
        else:
            messages.error(self.request, 'Something Wrong....')
            return super().get_redirect_url(*args, **kwargs)


class ToptracksCallbackView(RedirectView):
    permanent = True
    pattern_name = 'playlist:toptracks'

    def get_redirect_url(self, *args, **kwargs):
        if 'access_token' not in self.request.session :
            code = self.request.GET.get('code', None)
            result = upsert_toptracks('http://localhost:8000/playlist/toptracks/callback/', self.request, str(self  .request.user), code)
        else:
            result = upsert_toptracks('http://localhost:8000/playlist/toptracks/callback/', self.request, str(self.request.user))
        if result:
            messages.success(self.request, 'Update Successfully~')
            return super().get_redirect_url(*args, **kwargs)
        else:
            messages.error(self.request, 'Something Wrong....')
            return super().get_redirect_url(*args, **kwargs)


class TopartistsCallbackView(RedirectView):
    permanent = True
    pattern_name = 'playlist:topartists'

    def get_redirect_url(self, *args, **kwargs):
        if 'access_token' not in self.request.session :
            code = self.request.GET.get('code', None)
            result = upsert_topartists('http://localhost:8000/playlist/topartists/callback/', self.request, str(self.request.user), code)
        else:
            result = upsert_topartists('http://localhost:8000/playlist/topartists/callback/', self.request, str(self.request.user))

        if result:
            messages.success(self.request, 'Update Successfully~')
            return super().get_redirect_url(*args, **kwargs)
        else:
            messages.error(self.request, 'Something Wrong....')
            return super().get_redirect_url(*args, **kwargs)


class PlaylistView(View):

    def get(self, request, *args, **kwargs):
        playlists = get_lists(str(request.user))
        context = None
        if playlists:
            context = {"playlists": playlists["playlists"]}
        return render(request, template_name='playlists.html', context=context)


class PlaylistUpdate(LoginRequiredMixin, RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        what = self.request.POST['what']
        if what == 'playlist':
            redirect_uri = 'http://localhost:8000/playlist/callback/'
        elif what == 'toptrack':
            redirect_uri = 'http://localhost:8000/playlist/toptracks/callback/'
        elif what == 'topartist':
            redirect_uri = 'http://localhost:8000/playlist/topartists/callback/'

        scope = 'playlist-read-private playlist-read-collaborative user-top-read'
        self.url = unquote(get_auth(redirect_uri, scope))
        return super().get_redirect_url(*args, **kwargs)


class PlaylistTopTracks(View) :

    def get(self, request, *args, **kwargs):
        toptracks = get_toptracks(str(request.user))
        context = None
        if toptracks:
            context = {"toptracks": toptracks["toptracks"]}
        return render(request, template_name='toptracks.html', context=context)


class PlaylistTopArtists(View) :

    def get(self, request, *args, **kwargs):
        topartists = get_topartists(str(request.user))
        context = None
        if topartists:
            context = {"topartists": topartists["topartists"]}
        return render(request, template_name='topartists.html', context=context)
