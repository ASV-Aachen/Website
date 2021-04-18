from django.contrib import admin
#from .models import BlogEintrag
from web.models import infoPage, frontHeader, HeadPage, standartPages

admin.site.register(infoPage)
admin.site.register(HeadPage)
admin.site.register(frontHeader)

admin.site.register(standartPages)