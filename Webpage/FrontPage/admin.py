from django.contrib import admin
from ..Mitglieder.models import Profile
from ..FrontPage.models import Blogeintrag

# Register your models here.
# personen Kontrolle
admin.site.register(Profile)

# News
admin.site.register(Blogeintrag)