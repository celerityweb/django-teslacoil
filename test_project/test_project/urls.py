from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from teslacoil.site import TeslaSite
teslasite = TeslaSite()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tesla/', include(teslasite.urls)),
)
