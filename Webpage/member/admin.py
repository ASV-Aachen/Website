from django.contrib import admin
from .models import profile, position, position_in_the_club
# Register your models here.

admin.site.register(profile)
admin.site.register(position)
admin.site.register(position_in_the_club)