from django.contrib import admin
from .models import profile, Position, position_in_the_club
# Register your models here.

admin.site.register(profile)
admin.site.register(Position)
admin.site.register(position_in_the_club)