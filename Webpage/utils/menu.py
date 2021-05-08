from web.models import infoPage, HeadPage
from jollen.models import boot
from django import template

register = template.Library()

@register.simple_tag
def createMenuObject() -> {}:
    Themen = HeadPage.objects.all()

    Objects = []
    for Header in Themen:
        pages = infoPage.objects.filter(headPage=Header)

        zielObject = {
            "Header": Header,
            "seiten": pages,
        }

        Objects.append(zielObject)

    return Objects

@register.simple_tag
def createMenuObject_jollen() -> {}:

    return boot.objects.filter(isboat=True).order_by('klasse.name')

'''
To register in Template:
{% load menu %}

{% createMenuObject as menuObject %}

'''