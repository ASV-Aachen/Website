from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context, Template
from django.template.base import logger
from .models import blogPost
from django.http import HttpResponse
from django.contrib.auth.models import Permission
from django.conf import settings
import urllib.parse
import logging
import os
from .forms import newBlogEntry



# Alle News (TODO)
def News(request):
    try:
        Seite = request.GET.get('Seite', '')
        maxSeiten = request.GET['MaxSeiten']
        obersteNews = ((Seite-1)*5)

    except:
        Seite = 1
        obersteNews = 0
        idAnzahl = len(blogPost.objects.all())
        MaxSeiten = idAnzahl / 5

    return render(request, template_name="blog/News.html", context={
        "AktuelleID": Seite,
        "maxSeiten": MaxSeiten,
        "News": blogPost.objects.all().order_by('-id')[obersteNews:obersteNews + 5],
        #"UserLinks": GetMenu(request)
    })

    pass

# Die 5 TopNews für die Frontpage (Done)
def NewsforFrontPage(request):
    return render(request, "blog/includes/NewsFrontpage.html", context={
            "News": blogPost.objects.all().order_by('-id')[:5]
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
            'News': blogPost.objects.get(id=id),
        })
    except:
        return redirect("ASV")


'''Insert a new Blog Entry'''
def AddNews(request):
    if (request.user.is_authenticated):
        if request.method == "POST":
            form = newBlogEntry(request.POST, request.FILES)

            if form.is_valid():
                form.save(commit=False)
                form.instance.author = request.user.id
                form.save()

                return redirect("ASV")
        else:
            form = newBlogEntry()
        return render(request, "blog/AddNews.html", {"form": form})
    else:
        return redirect("ASV")
