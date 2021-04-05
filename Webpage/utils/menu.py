from web.models import infoPage
from django import template

register = template.Library()

@register.simple_tag
def createMenuObject() -> {}:
    Themen = infoPage.themen

    Objects = []
    for kennung, titel in Themen:
        pages = infoPage.objects.filter(status=kennung)

        zielObject = {
            "titel": titel,
            "seiten": pages,
            "kennung": kennung
        }

        Objects.append(zielObject)

    return Objects



'''
To register in Template:
{% load menu %}

{% createMenuObject as menuObject %}

'''