from functools import reduce

from django.db.models import F
from django.db.models.functions import Coalesce

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context, Template
from django.template.base import logger
from django.http import HttpResponse


# Create your views here.
from django.views.generic import DeleteView

from django.urls import resolve
from .forms import CruiseForm
from .models import Cruise
from .utils import get_aktuelle_saison, check_authentication_redirect_if_fails
from member.models import profile


def cruises_home(request):

    cruises = Cruise.objects.all()
    return render(request, "cruises/cruises_home.html", context={
        "cruises": cruises
    })

def ship_position(request):

    return render(request, "cruises/ship_position.html")

def createNewCruise(request):
    check_authentication_redirect_if_fails(request)

    if request.method == "POST":
        form = CruiseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cruises_home")
    else:
        form = CruiseForm(initial={'MaxBerths': 12})
    return render(request, "cruises/cruise_form.html", {"form": form, "model_name": "Cruise"})

def cruise_edit(request):
    if (request.user.is_authenticated):
        if request.method == "POST":
            form = CruiseForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                if request.GET['pk'] != "":
                    if (Cruise.objects.filter(id = request.GET['pk']).exists()):
                        actualCruise = Cruise.objects.filter(id = request.GET['pk'])[0]
                        form.instance.id = request.GET['pk']
                form.save()
                return redirect("cruises_home")
        else:
            if ('pk' in request.GET):
                pk = request.GET['pk']
                # Load data from ID
                if(Cruise.objects.filter(id=pk).exists()):
                    cruise = Cruise.objects.get(id=pk)
                    form = CruiseForm(instance=cruise)
                    return render(request, "cruises/cruise_form.html", {"form": form, "cruise": cruise})
                else:
                    form = CruiseForm(initial={'MaxBerths': 9})
                    return render(request, "cruises/cruise_form.html", {"form": form})
            else:
                form = CruiseForm(initial={'MaxBerths': 8})
                return render(request, "cruises/cruise_form.html", {"form": form})
    else:
        return redirect("ASV")

def cruise_delete(request, pk):
    return model_delete(
        request,
        pk,
        Cruise,
        "cruises_home",
        None
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