from django.contrib import admin

# Register your models here.
from .models import Boot, Tag, Arbeitskategorie, Arbeitsstundenausschreibung

admin.site.register(Boot)
admin.site.register(Arbeitskategorie)
admin.site.register(Tag)
admin.site.register(Arbeitsstundenausschreibung)
