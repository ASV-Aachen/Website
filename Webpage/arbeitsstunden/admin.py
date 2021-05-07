from django.contrib import admin

# Register your models here.
from .models import Projekt, Tag, Arbeitsstundenausschreibung, Saison, Arbeitsbeteiligung, Arbeitseinheit

admin.site.register(Projekt)
admin.site.register(Tag)
admin.site.register(Arbeitsstundenausschreibung)
admin.site.register(Saison)
admin.site.register(Arbeitsbeteiligung)
admin.site.register(Arbeitseinheit)