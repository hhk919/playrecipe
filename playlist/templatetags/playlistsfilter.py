from django import template

register = template.Library()

@register.filter
def get_name_w_url(artists) :
    return ', '.join(['<a href="'+artist['external_urls']['spotify']+'">'+artist['name']+'</a>' for artist in artists])

@register.filter
def get_name(artists) :
    return ', '.join([artist['name'] for artist in artists])

@register.filter
def get_genre(genres):
    return ', '.join(genre for genre in genres)