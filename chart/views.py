from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from chart.services import get_fav_artists, get_fav_genres, get_topartists_avg, get_toptracks_avg, check


class ChartView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        username = str(request.user)
        check1, check2 = check(username)
        toptracks_avg = list(get_toptracks_avg(username))[0]['avgPopularity'] if check1 else None
        fav_artists = list(get_fav_artists(username)) if check1 else None
        topartists_avg = list(get_topartists_avg(username))[0]['avgPopularity'] if check2 else None
        fav_genres = list(get_fav_genres(username)) if check2 else None

        context = {'topartists_avg': topartists_avg, 'toptracks_avg': toptracks_avg, 'fav_genres': fav_genres,
                   'fav_artists': fav_artists}
        return render(request, "charts.html", context)
