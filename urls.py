from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin


admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
    url(r'admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    url(
        r'^admin/',
        include(admin.site.urls),
    ),
    url(
        r'^',
        include('registration.urls')
    ),
    url(
        r'^home/',
        include('home.urls')
    ),
    url(
        r'^purchasing/',
        include('purchasing.urls')
    ),
    url(
        r'^management/',
        include('management.urls')
    ),
    url(
        r'^storage/',
        include('storage.urls')
    ),
    url(
        r'^news/',
        include('news.urls')
    ),
)

urlpatterns += patterns('', url(r'tinymce/', include('tinymce.urls')),)
urlpatterns += patterns('', url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),)
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
        urlpatterns += patterns('',
        url(r'media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        )
