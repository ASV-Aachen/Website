from web.models import InfoPage


def createMenuObject() -> {}:
    Themen = InfoPage.themen

    Objects = []
    for kennung, titel in Themen:
        pages = InfoPage.objects.filter(status=kennung)

        zielObject = {
            "titel": titel,
            "seiten": pages,
            "kennung": kennung
        }

        Objects.append(zielObject)

    return Objects