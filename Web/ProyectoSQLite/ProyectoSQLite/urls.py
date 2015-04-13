from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^maquinas/', include('maquinas.urls', namespace="maquinas")),
    url(r'^admin/', include(admin.site.urls)),
]
