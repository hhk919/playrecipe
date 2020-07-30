from chart.repositories import ChartDAO


def check(username):
    return ChartDAO().check(username)


def get_toptracks_avg(username):
    return ChartDAO().get_toptracks_avg(username)


def get_topartists_avg(username):
    return ChartDAO().get_topartists_avg(username)


def get_fav_genres(username):
    return ChartDAO().get_fav_genres(username)


def get_fav_artists(username):
    return ChartDAO().get_fav_artists(username)
