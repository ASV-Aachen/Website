from functools import reduce

from django.db.models import F
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import DeleteView

from django.urls import resolve
from cruises.forms import CruiseForm
from cruises.utils import get_aktuelle_saison, check_authentication_redirect_if_fails
from member.models import profile


def cruises_home(request):
    
    return render(request, "cruises/cruises_home.html",)

def createNewCruise(request):
    check_authentication_redirect_if_fails(request)

    if request.method == "POST":
        form = CruiseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cruises_home")
    else:
        form = CruiseForm(initial={'MaxBerths': 12})
    return render(request, "cruises/cruise_form.html", {
        "form": form,
        "model_name": "Cruise",
        "delete_view_name": "cruise_delete"
    })

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