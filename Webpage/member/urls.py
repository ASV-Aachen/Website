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

app_name: "member"

urlpatterns = [
    path('', views.index, name="MeinASV"),
    path('Mitgliederverzeichnis', views.member_directory, name="Mitgliederverzeichnis"),
    path('User/<str:id>', views.single_user, name="User"),
    path('Einstellungen', views.settings, name="Einstellungen"),
    path('Kalender', views.kalender, name='Kalender'),

    path('Menu', views.memberMenu, name="MemberMenu"),
    path('Menu/allMembers', views.alleMember, name="allMembers"),
    path('Menu/export', views.exportPage, name ="allMembers_Export"),
    path('Menu/editor', views.newMemberEditor, name ="memberEditor"),
    path('Menu/import', views.massenimport, name ="memberImport"),
    path('Menu/delete', views.deleteUser, name="memberDelete"),
    path('Menu/edit/<str:id>', views.editUserAsSchriftward, name="memberEdit")
]