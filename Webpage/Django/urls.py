from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from filebrowser.sites import site
from ajax_select import urls as ajax_select_urls
from web.views import upload_image

urlpatterns = [
    path('', include('web.urls')),
    path('admin/', admin.site.urls),
    path('news/', include('blog.urls')),
    path('mitglieder/', include('member.urls')),
    path('admin/filebrowser/', site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('upload_image/', upload_image),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('jollen/', include('jollen.urls')),
    path('cruises/', include('cruises.urls')),
    url(r'^ajax_select/', include(ajax_select_urls)),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

