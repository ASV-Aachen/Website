from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template import Context, Template
from django.template.base import logger
from .models import BlogEintrag
from django.http import HttpResponse
from django.contrib.auth.models import Permission
from django.conf import settings
import urllib.parse
import logging
import os




# Alle News (TODO)
def News(request):
    try:
        Seite = request.GET.get('Seite', '')
        maxSeiten = request.GET['MaxSeiten']
        obersteNews = ((Seite-1)*5)

    except:
        Seite = 1
        obersteNews = 0
        idAnzahl = len(BlogEintrag.objects.all())
        MaxSeiten = idAnzahl / 5

    return render(request, template_name="blog/News.html", context={
        "AktuelleID": Seite,
        "maxSeiten": MaxSeiten,
        "News": BlogEintrag.objects.all().order_by('-id')[obersteNews:obersteNews+5],
        #"UserLinks": GetMenu(request)
    })

    pass

# Die 5 TopNews für die Frontpage (Done)
def NewsforFrontPage(request):
    return render(request, "blog/includes/NewsFrontpage.html", context={
            "News": BlogEintrag.objects.all().order_by('-id')[:5]
    })
    



# Einzelne News Page (DONE)
def SingleNews(request):
    """
    Je nach ID gibt das System eine spezielle News zurück.
    Alle News müssen Offen sein
    :param request:
    :return:
    """
    try:
        id = request.GET.get('id', '')
        return render(request, template_name="blog/newsPage.html", context={
            'News': BlogEintrag.objects.get(id=id), 
            "UserLinks": GetMenu(request)
        })
    except:
        return redirect("ASV")

def AddNews(request):
    if request.user.is_authenticated:
        if request.POST:
            # Neue Nachricht eingefügt
            User = request.user
            Titel = request.POST['Titel']
            Text = request.POST['Text']
            Datum = date.today()

            NewText = BlogEintrag(Titel=Titel, Text=Text, Autor=User, Datum=Datum)
            NewText.save()
            pass
        if request.GET:
            # Editor
            return render(request, template_name="blog/AddNews.html")
            pass
    else:
        return redirect('ASV')
