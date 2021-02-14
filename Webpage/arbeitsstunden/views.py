from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import DeleteView

from arbeitsstunden.forms import ArbeitsstundenausschreibungForm
from arbeitsstunden.models import Arbeitsstundenausschreibung
from django.urls import resolve


def arbeitsstundenausschreibung(request):
    if request.user.is_authenticated:
        ausschreibungen = Arbeitsstundenausschreibung.objects.all()
        print(ausschreibungen)
        return render(request, "arbeitsstunden/arbeitsstundenausschreibung_index.html", context={
            "ausschreibungen": ausschreibungen
        })
    else:
        redirect("/")


def createNewAusschreibung(request):
    if request.method == "POST":
        form = ArbeitsstundenausschreibungForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/arbeitsstunden")
    else:
        form = ArbeitsstundenausschreibungForm()
    return render(request, "arbeitsstunden/ausschreibung_edit.html", {"form": form})


def editAusschreibung(request, pk):
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
    ausschreibung = get_object_or_404(Arbeitsstundenausschreibung, pk=pk)
    ausschreibung.delete()
    return redirect("/arbeitsstunden")