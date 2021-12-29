from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(cruise)
admin.site.register(sailor)
admin.site.register(cruiseShare)