from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin


admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
    url(
        r'^home/',
        include('home.urls')
    ),
    url(
        r'^purchasing/',
        include('purchasing.urls')
    ),
)

urlpatterns += patterns('', url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),)
