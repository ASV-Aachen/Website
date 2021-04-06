from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context, Template
from django.template.base import logger
from .models import blogPost, blogPostHistory
from django.http import HttpResponse
from django.contrib.auth.models import Permission
from django.conf import settings
import urllib.parse
import logging
import os
from .forms import newBlogEntry
from django.core.paginator import Paginator
from utils.loginFunctions import isUserPartOfGroup


# Alle News
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

'''writerView'''
@user_passes_test(isUserPartOfGroup(groupNameArray = ['Editor']))
@login_required
def adminNewsPage(request):
    posts = blogPost.objects.all().order_by('-id')
    paginator = Paginator(posts, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/editorNewsPage.html', {'page_obj': page_obj})


''' News für Löschung markieren'''
@user_passes_test(isUserPartOfGroup(groupNameArray = ['Editor']))
@login_required
def deleteNews(request):
    if (request.user.is_authenticated):
        if ('id' in request.GET):
            id = request.GET['id']
            blogPost.objects.get(id=id).delete()
        return redirect("writerView")
    else:
        return redirect("ASV")

'''Insert a new Blog Entry'''
@user_passes_test(isUserPartOfGroup(groupNameArray = ['Editor']))
@login_required
def AddNews(request):
    if (request.user.is_authenticated):

        if request.method == "POST":
            # Eintragen in die DB
            form = newBlogEntry(request.POST, request.FILES)

            if form.is_valid():
                # abspeichern
                form.save(commit=False)
                if request.GET['id'] != "":
                    if (blogPost.objects.filter(id = request.GET['id']).exists()):
                        # if Data exits: setze den last author anders
                        aktuellerPost = blogPost.objects.filter(id = request.GET['id'])[0]

                        # setze den alten Text als History
                        newhistory = blogPostHistory(titel=aktuellerPost.titel, text=aktuellerPost.text, editor=request.user.first_name + " " + request.user.last_name)
                        newhistory.save()
                        aktuellerPost.history.add(newhistory)

                        form.instance.author_id = aktuellerPost.author.id
                        form.instance.last_editor = request.user.first_name + " " + request.user.last_name
                        form.instance.id = request.GET['id']
                    else:
                        # Data existiert noch nicht, also setzen wir anders
                        form.instance.author_id = request.user.id
                        form.instance.last_editor = request.user.first_name + " " + request.user.last_name

                        # setze den neuen Text als erste History
                        newhistory = blogPostHistory(titel=request.titel, text=request.text, editor=request.user.first_name + " " + request.user.last_name)
                        newhistory.save()
                        request.history.add(newhistory)
                else:
                    # Data existiert noch nicht, also setzen wir anders
                    form.instance.author_id = request.user.id
                    form.instance.last_editor = request.user.first_name + " " + request.user.last_name

                    # setze den neuen Text als erste History
                    newhistory = blogPostHistory(titel=request.titel, text=request.text,
                                                 editor=request.user.first_name + " " + request.user.last_name)
                    newhistory.save()
                    request.history.add(newhistory)

                form.save()

                return redirect("writerView")
        else:
            # Formular laden

            if ('id' in request.GET):
                id = request.GET['id']
                # ID gegeben, also Daten laden
                if(blogPost.objects.filter(id=id).exists()):
                    # ID existiert, also zurückgeben
                    post = blogPost.objects.get(id=id)

                    if('version' in request.GET):
                        # Wir suchen nach einer bestimten Version
                        versionID = request.GET['version']
                        if post.history.filter(id = versionID).exists():
                            OldPost = post.history.get(id = request.GET['version'])
                            post.titel = OldPost.titel
                            post.text = OldPost.text

                    form = newBlogEntry(instance=post)
                    hist = post.history.all().order_by('-id')
                    return render(request, "blog/AddNews.html", {"form": form, "post": post, "hist": hist})
                else:
                    # ID ist zwar gegeben, existiert aber nicht
                    return redirect("writerView")

            else:
                # Keine ID gegeben, neuen Artikel anlegen
                form = newBlogEntry()
                return render(request, "blog/AddNews.html", {"form": form})

    else:
        return redirect("ASV")
