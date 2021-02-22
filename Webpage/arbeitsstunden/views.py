from functools import reduce

from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import DeleteView

from Mitglieder.models import Profile
from arbeitsstunden.forms import ArbeitsstundenausschreibungForm
from arbeitsstunden.models import Arbeitsstundenausschreibung, Arbeitsbeteiligung, Saison, Projekt, Arbeitseinheit
from django.urls import resolve

from arbeitsstunden.utils import get_aktuelle_saison, check_authentication_redirect_if_fails


def arbeitsstunden_home(request):
    check_authentication_redirect_if_fails(request)

    user = request.user
    profile = Profile.objects.get(user=user)
    aktuelle_saison = get_aktuelle_saison()
    beteiligungen_aktuelle_saison = Arbeitsbeteiligung.objects.filter(Arbeitsleistender=profile,
                                                                      Arbeitseinheit__Projekt__Saison__Jahr=aktuelle_saison.Jahr)

    geleistete_stunden = sum(beteiligung.Arbeitszeit for beteiligung in beteiligungen_aktuelle_saison)
    soll_arbeitsstunden = 40
    anteil_arbeitsstunden_erledigt_prozent = int((geleistete_stunden / soll_arbeitsstunden) * 100)

    return render(request, "arbeitsstunden/arbeitsstunden_home.html", context={
        "beteiligungen": beteiligungen_aktuelle_saison,
        "geleisteteArbeitsstunden": geleistete_stunden,
        "soll_arbeitsstunden": soll_arbeitsstunden,
        "anteil_arbeitsstunden_erledigt_prozent": anteil_arbeitsstunden_erledigt_prozent
    })


def projekte_overview(request):
    check_authentication_redirect_if_fails(request)

    saisons = Saison.objects.all()
    projekte = []
    for saison in saisons:
        projects_in_season = Projekt.objects.filter(Saison=saison)
        projekte.append({
            "saison": saison,
            "projekte": projects_in_season
        })

    return render(request, "arbeitsstunden/projekte_overview.html", context={
        "projekte": projekte
    })

def projekte_detail(request, pk):
    check_authentication_redirect_if_fails(request)

    projekt = get_object_or_404(Projekt, pk=pk)
    arbeitseinheiten = Arbeitseinheit.objects.filter(Projekt=projekt)
    return render(request, "arbeitsstunden/projekte_details.html", context={
        "projekt": projekt,
        "arbeitseinheiten": arbeitseinheiten
    })

def arbeitseinheit_details(request, pk):
    check_authentication_redirect_if_fails(request)

    arbeitseinheit = get_object_or_404(Arbeitseinheit, pk=pk)
    arbeitsbeteiligungen = arbeitseinheit.Beteiligte.through.objects.all()
    return render(request, "arbeitsstunden/arbeitseinheit_details.html", context={
        "arbeitseinheit": arbeitseinheit,
        "arbeitsbeteiligungen": arbeitsbeteiligungen
    })


def ausschreibungen_overview(request):
    check_authentication_redirect_if_fails(request)

    ausschreibungen = Arbeitsstundenausschreibung.objects.all()
    print(ausschreibungen)
    return render(request, "arbeitsstunden/ausschreibungen_overview.html", context={
        "ausschreibungen": ausschreibungen
    })



def createNewAusschreibung(request):
    check_authentication_redirect_if_fails(request)

    if request.method == "POST":
        form = ArbeitsstundenausschreibungForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/arbeitsstunden")
    else:
        form = ArbeitsstundenausschreibungForm()
    return render(request, "arbeitsstunden/ausschreibung_edit.html", {"form": form})


def editAusschreibung(request, pk):
    check_authentication_redirect_if_fails(request)

    ausschreibung = get_object_or_404(Arbeitsstundenausschreibung, pk=pk)
    if request.method == "POST":
        form = ArbeitsstundenausschreibungForm(request.POST, instance=ausschreibung)
        if form.is_valid():
            ausschreibung.save()
            form.save()
            return redirect('/arbeitsstunden')
    else:
        form = ArbeitsstundenausschreibungForm(instance=ausschreibung)
    return render(request, 'arbeitsstunden/ausschreibung_edit.html', {'form': form})


def deleteAusschreibung(request, pk):
    check_authentication_redirect_if_fails(request)

    ausschreibung = get_object_or_404(Arbeitsstundenausschreibung, pk=pk)
    ausschreibung.delete()
    return redirect("/arbeitsstunden")