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
    path('', views.dashboard, name="arbeitsstunden_home"),

    path('projekte', views.allAktivProjekts, name="projekte_overview"),
    path('projekte/<int:projectID>', views.showProjekt, name="projekte_detail"),
    path('projekte/new', views.newProjekt, name="projekt_new"),
    path('projekte/edit/<int:projectID>', views.editProjekt, name='projekt_edit'),
    path('projekte/delete/<int:projectID>', views.deleteProjekt, name='projekt_delete'),

    path('subproject/new', views.newSubprojekt, name="newSubprojekt"),
    path('subproject/new/<int:idProject>', views.newSubprojectToProject, name="newSubprojectToProject"),
    path('subproject/edit/<int:idSubproject>', views.editSubproject, name='editSubproject'),
    path('subproject/delete/<int:idSubproject>', views.deleteSubproject, name='deleteSubproject'),

    path('season', views.seasonOverview, name="seasonOverview"),
    path('season/<int:seasonID>', views.singleSeasonOverview, name="singleSeasonOverview"),

    path('costCenter', views.costCenterOverview, name="costCenterOverview"),
    path('singleCostCenterOverview/<int:centerID>', views.singleCostCenterOverview, name="singleCostCenterOverview"),
]