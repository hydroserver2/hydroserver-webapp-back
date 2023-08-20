from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from sites.api import api
from hydroserver.views import index

from core.api import management_api
from accounts.api import accounts_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sensorthings/', include('sensorthings.urls')),
    path('api/', api.urls),
    path('api/data/', management_api.urls),
    path('api/account/', accounts_api.urls),
    re_path('.*', index),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
