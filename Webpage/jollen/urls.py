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

from django.urls import path
from . import views

app_name: "jollen"

urlpatterns = [
    path('', views.ubersicht, name="jollenÜbersicht"),
    path('<str:name>', views.description, name="jollen_description"),
    path('<str:name>/status', views.settings_status, name="jollen_settings_status"),
    path('<str:name>/description', views.settings_description, name="jollen_settings_description"),
]