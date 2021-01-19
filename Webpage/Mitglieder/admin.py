from django.contrib import admin
from .models import Profile, Status, Position, PositionImVerein
# Register your models here.

admin.site.register(Profile)
admin.site.register(Status)
admin.site.register(Position)
admin.site.register(PositionImVerein)