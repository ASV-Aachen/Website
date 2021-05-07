import datetime

from django.shortcuts import redirect

from arbeitsstunden.models import Saison

SEASON_BEGIN_MONTH = 7  # Juli


def get_aktuelle_saison():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    season_year = year if month >= SEASON_BEGIN_MONTH else year - 1
    saison = Saison.objects.get(Jahr=season_year)
    return saison


def check_authentication_redirect_if_fails(request, redirect_location="/"):
    if not request.user.is_authenticated:
        redirect(redirect_location)
