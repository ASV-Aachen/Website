from web.models import infoPage


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