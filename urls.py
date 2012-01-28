from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^upload/$', 'main.views.import_spreadsheet', 
        name='import_spreadsheet'),
    url(r'^download/(?P<path>[a-zA-Z0-9]+)/$', 
        'main.views.download_spreadsheet',
        name='download_spreadsheet'),
    # url(r'^skel/', include('skel.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
