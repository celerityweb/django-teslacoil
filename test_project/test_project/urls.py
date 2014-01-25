from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from teslacoil.site import TeslaSite
teslasite = TeslaSite()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tesla/', include(teslasite.urls)),

    url(r'^tests/make_message/', 'test_project.views.add_message_view',
        name='add-message'),
    url(r'^tests/noop_view/', 'test_project.views.noop_view',
        name='noop-view')
)
