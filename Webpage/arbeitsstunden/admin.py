from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(season)
admin.site.register(account)
admin.site.register(costCenter)
admin.site.register(project)
admin.site.register(work)
