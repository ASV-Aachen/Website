from django.urls import path, include
from . import views

app_name: "cruises"


urlpatterns = [
    path('', views.cruises_home, name="cruises_home")
]