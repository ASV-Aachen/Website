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

app_name: "web"

# TODO: Mein ASV sollte natürlich der interne Bereich sein, Mitglieder muss noch umgesetzt werden

urlpatterns = [
    path('', views.MainPage, name="ASV"),
    path('login', views.loginFunction, name="login"),
    path('logout', views.logoutFunktion, name="logout"),
    # path('UserTestPage', views.UserTest, name="UserTests"),
    path('unfertig', views.unfertig, name='unfertig'),
    path('errorPage', views.errorPage, name='errorPage'),
    path('autopopulate', views.autoPopulate, name='autoPopulate'),
    path('info', views.InfoPageView, name="info"),
    path('sponsoren', views.show_all_Sponsor, name="sponsor"),

    path('info/<str:theme>', views.infoPage_singleHeader, name="InfoPage_Header"),
    path('info/<str:theme>/<str:name>', views.infoPage_singlePage, name="InfoPage"),

    path("infoEditor", views.infoPageEditor, name="InfoEditor"),
    path("InfoEditor_Header", views.infoPageEditor_Header, name="InfoEditor_Header"),

    path("infoMenu", views.infoPageMenu, name="infoMenu"),

    path('impressum', views.impressum, name="impressum"),
    path('datenschutz', views.datenschutz, name="datenschutz")
]