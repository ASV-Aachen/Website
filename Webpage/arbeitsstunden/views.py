from functools import reduce

from django.db.models import F
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import DeleteView

from arbeitsstunden.forms import ArbeitsstundenausschreibungForm, ProjectForm, ArbeitseinheitForm, \
    ArbeitsbeteiligungForm
from arbeitsstunden.models import Arbeitsstundenausschreibung, Arbeitsbeteiligung, Saison, Projekt, Arbeitseinheit
from django.urls import resolve

from arbeitsstunden.utils import get_aktuelle_saison, check_authentication_redirect_if_fails
from member.models import profile


def arbeitsstunden_home(request):
    check_authentication_redirect_if_fails(request)

    user = request.user
    userprofile = profile.objects.get(user=user)
    aktuelle_saison = get_aktuelle_saison()
    beteiligungen_aktuelle_saison = Arbeitsbeteiligung.objects. \
        filter(Arbeitsleistender=userprofile, Arbeitseinheit__Projekt__Saison__Jahr=aktuelle_saison.Jahr). \
        order_by(F("Arbeitseinheit__Datum").desc())

    geleistete_stunden = sum(beteiligung.Arbeitszeit for beteiligung in beteiligungen_aktuelle_saison)
    soll_arbeitsstunden = 40
    anteil_arbeitsstunden_erledigt_prozent = min(100, int((geleistete_stunden / soll_arbeitsstunden) * 100))

    return render(request, "arbeitsstunden/arbeitsstunden_home.html", context={
        "beteiligungen": beteiligungen_aktuelle_saison,
        "geleisteteArbeitsstunden": geleistete_stunden,
        "soll_arbeitsstunden": soll_arbeitsstunden,
        "anteil_arbeitsstunden_erledigt_prozent": anteil_arbeitsstunden_erledigt_prozent
    })


def ausschreibung_details(request, pk):
    check_authentication_redirect_if_fails(request)

    ausschreibung = get_object_or_404(Arbeitsstundenausschreibung, pk=pk)
    return render(request, "arbeitsstunden/ausschreibung_details.html", context={
        "ausschreibung": ausschreibung
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


def model_new(request, model_display_name, form_type, initial_get_arguments_names, redirect_function):
    check_authentication_redirect_if_fails(request)

    initial_values = {}
    for name in initial_get_arguments_names:
        initial_values[name] = int(request.GET.get(name, None)) if request.GET.get(name, None) is not None else None

    if request.method == "POST":
        form = form_type(request.POST)
        if form.is_valid():
            model = form.save()
            return redirect_function(model)
    else:
        form = form_type()
        for name in initial_get_arguments_names:
            if initial_values[name] is not None:
                form.fields[name].initial = initial_values[name]

    return render(request, "arbeitsstunden/form_template.html", {
        "form": form,
        "model_name": model_display_name
    })


def arbeitseinheit_new(request):
    return model_new(
        request,
        "Arbeitseinheit",
        ArbeitseinheitForm,
        ["Projekt"],
        lambda arbeitseinheit: redirect("arbeitseinheit_details", pk=arbeitseinheit.id)
    )


def createNewAusschreibung(request):
    check_authentication_redirect_if_fails(request)

    if request.method == "POST":
        form = ArbeitsstundenausschreibungForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ausschreibungen_overview")
    else:
        form = ArbeitsstundenausschreibungForm()
    return render(request, "arbeitsstunden/form_template.html", {
        "form": form,
        "model_name": "Arbeitsstundenausschreibung",
        "delete_view_name": "ausschreibung_delete"
    })


def model_edit(request, pk, model_type, model_display_name, form_type, model_details_page_redirect_lambda, delete_page_name):
    check_authentication_redirect_if_fails(request)

    model = get_object_or_404(model_type, pk=pk)
    if request.method == "POST":
        form = form_type(request.POST, instance=model)
        if form.is_valid():
            model.save()
            form.save()
            return model_details_page_redirect_lambda(model)
    else:
        form = form_type(instance=model)
    return render(request, 'arbeitsstunden/form_template.html', {
        'form': form,
        'model_name': model_display_name,
        "delete_view_name": delete_page_name
    })


def arbeitseinheit_edit(request, pk):
    return model_edit(
        request,
        pk,
        Arbeitseinheit,
        "Arbeitseinheit",
        ArbeitseinheitForm,
        lambda arbeitseinheit : redirect("arbeitseinheit_details", pk=arbeitseinheit.id),
        "arbeitseinheit_delete"
    )


def ausschreibungen_overview(request):
    check_authentication_redirect_if_fails(request)

    ausschreibungen = Arbeitsstundenausschreibung.objects.all()
    print(ausschreibungen)
    return render(request, "arbeitsstunden/ausschreibungen_overview.html", context={
        "ausschreibungen": ausschreibungen
    })


def project_new(request):
    return model_new(
        request,
        "Projekt",
        ProjectForm,
        [],
        lambda projekt: redirect("projekte_detail", pk=projekt.id)
    )


def projekt_edit(request, pk):
    return model_edit(
        request,
        pk,
        Projekt,
        "Projekt",
        ProjectForm,
        lambda projekt : redirect("projekte_detail", pk=projekt.id),
        "projekt_delete"
    )


def projekt_delete(request, pk):
    return model_delete(
        request,
        pk,
        Projekt,
        "projekte_overview"
    )


def edit_ausschreibung(request, pk):
    return model_edit(
        request,
        pk,
        Arbeitsstundenausschreibung,
        "Arbeitsstundenausschreibung",
        ArbeitsstundenausschreibungForm,
        lambda ausschreibung: redirect("ausschreibung_details", pk=ausschreibung.id),
        "ausschreibung_delete"
    )


def model_delete(request, pk, model_type, overview_page_name, parent_model_name = None):
    check_authentication_redirect_if_fails(request)

    model = get_object_or_404(model_type, pk=pk)

    if parent_model_name is not None:
        parent_id = getattr(model, parent_model_name).id
    
    model.delete()
    if parent_model_name is None:
        return redirect(overview_page_name)
    else:
        return redirect(overview_page_name, pk=parent_id)


def deleteAusschreibung(request, pk):
    return model_delete(
        request,
        pk,
        Arbeitsstundenausschreibung,
        "ausschreibungen_overview"
    )

def arbeitsbeteiligung_new(request):
    return model_new(
        request,
        "Arbeitsbeteiligung",
        ArbeitsbeteiligungForm,
        ["Arbeitseinheit"],
        lambda beteiligung: redirect("arbeitseinheit_details", pk=beteiligung.Arbeitseinheit.id)
    )

def arbeitsbeteiligung_edit(request, pk):
    return model_edit(
        request,
        pk,
        Arbeitsbeteiligung,
        "Arbeitsbeteiligung",
        ArbeitsbeteiligungForm,
        lambda arbeitsbeteiligung : redirect("arbeitseinheit_details", pk=arbeitsbeteiligung.Arbeitseinheit.id),
        "arbeitsbeteiligung_delete"
    )

def arbeitsbeteiligung_delete(request, pk):
    return model_delete(
        request,
        pk,
        Arbeitsbeteiligung,
        "arbeitseinheit_details",
        "Arbeitseinheit"
    )

def arbeitseinheit_delete(request, pk):
    return model_delete(
        request,
        pk,
        Arbeitseinheit,
        "projekte_detail",
        "Projekt"
    )