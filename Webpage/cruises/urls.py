"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views

app_name: "cruises"


urlpatterns = [
    path('', views.overview, name="cruisesOverview"),
    path('cruisesOverview', views.overview, name="cruisesOverview"),
    path('cruisesOverview/<int:id>', views.overview, name="cruisesOverview"),
    path('cruisesOverview/<int:year>/<int:id>', views.overview, name="cruisesOverview"),
    path('cruisesOverview/<int:year>', views.overview, name="cruisesOverview"),
    path('sailorOverview', views.sailorOverview, name="sailorOverview"),
    path('newCruise', views.newCruise, name="newCruise"),
    path('editCruise', views.editCruise, name="editCruise"),
    path('deleteCruise', views.deleteCruise, name="deleteCruise"),
    path('deleteCruiseShare', views.deleteCruiseShare, name="deleteCruiseShare"),
    path('makeCrew', views.makeCrew, name="makeCrew"),
    path('makeWatch', views.makeWatch, name="makeWatch"),
    path('makeSkipper', views.makeSkipper, name="makeSkipper"),
    path('setWatch', views.setWatch, name="setWatch"),
    path('setSkipper', views.setSkipper, name="setSkipper")
]