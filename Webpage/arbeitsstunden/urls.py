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
    path('/', views.arbeitsstunden_home, name="arbeitsstunden_home"),
    path('/ausschreibungen', views.ausschreibungen_overview, name="ausschreibungen_overview"),
    path('ausschreibungen/new', views.createNewAusschreibung, name="ausschreibung_new"),
    path('ausschreibungen/edit/<int:pk>', views.editAusschreibung, name='ausschreibung_edit'),
    path('ausschreibungen/delete/<int:pk>', views.deleteAusschreibung, name='ausschreibung_delete'),

    path('/projekte', views.projekte_overview, name="projekte_overview"),
    path('/projekte/<int:pk>', views.projekte_detail, name="projekte_detail"),
    path('/arbeitseinheit/<int:pk>', views.arbeitseinheit_details, name="arbeitseinheit_details")
]