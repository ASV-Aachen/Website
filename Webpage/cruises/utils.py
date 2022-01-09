import datetime

from django.shortcuts import redirect

SEASON_END_MONTH = 7  # Juli


def get_aktuelle_saison():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    return year

def check_authentication_redirect_if_fails(request, redirect_location="/"):
    if not request.user.is_authenticated:
        redirect(redirect_location)