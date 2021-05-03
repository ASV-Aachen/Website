from django.urls import path, include
from . import views

app_name: "cruises"


urlpatterns = [
    path('', views.cruises_home, name="cruises_home"),
    path('cruises/new', views.createNewCruise, name="cruise_new"),
    ##path('cruises/edit/<int:pk>', views.cruise_edit, name="cruise_edit"),
    path('cruises/edit', views.cruise_edit, name="cruise_edit"),
    path('cruises/ship_position', views.ship_position, name="ship_position")
]