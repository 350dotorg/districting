from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^upload/$', 'main.views.import_spreadsheet', name='import_spreadsheet'),
    # url(r'^skel/', include('skel.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
