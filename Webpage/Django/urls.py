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
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from filebrowser.sites import site
from ajax_select import urls as ajax_select_urls


urlpatterns = [
    path('', include('web.urls')),
    path('admin/', admin.site.urls),
    path('arbeitsstunden/', include('arbeitsstunden.urls')),
    path('news/', include('blog.urls')),
    path('mitglieder/', include('member.urls')),
    path('admin/filebrowser/', site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('jollen/', include('jollen.urls')),
    url(r'^ajax_select/', include(ajax_select_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

