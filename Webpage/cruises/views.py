from functools import reduce

from django.db.models import F
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import DeleteView

from django.urls import resolve
from member.models import profile


def cruises_home(request):
    
    return render(request, "cruises/cruises_home.html",)
    

