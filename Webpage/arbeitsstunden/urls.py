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

app_name: "arbeitsstunden"


urlpatterns = [
    #path('', views.dashboard, name="arbeitsstunden_home"),

    path('', views.overview, name="arbeitsstundenOverview"),

    path('projekte', views.allAktivProjekts, name="projekte_overview"),
    path('projekte/<int:projectID>', views.showProjekt, name="projekte_detail"),
    path('projekte/new', views.newProjekt, name="projekt_new"),
    path('projekte/edit/<int:projectID>', views.editProjekt, name='projekt_edit'),
    path('projekte/delete/<int:projectID>', views.deleteProjekt, name='projekt_delete'),

    path('projecte/<int:projectID>/work/add', views.addWork, name="addWork"),
    path('projecte/<int:workID>/work/edit', views.editWork, name="editWork"),
    path('projecte/<int:workID>/work/delete', views.deleteWork, name="deleteWork"),

    path('season', views.seasonOverview, name="seasonOverview"),
    path('season/<int:year>', views.singleSeasonOverview, name="singleSeasonOverview"),

    path('costCenter', views.costCenterOverview, name="costCenterOverview"),
] 