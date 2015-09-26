
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from registration import views as registration_views
from const import IDENTITYERROR

from django.contrib.auth import views as auth_views
urlpatterns = patterns('',
    url(
        r'^$',auth_views.login,{'template_name':'login.html'}
    ),
    url(
        r'^identityerror$',auth_views.login,{'template_name':'login.html','extra_context':{'identityerror':IDENTITYERROR}}
    ),
    url(
        r'^logout$',
        auth_views.logout,{'next_page':'/logoutredirect'}
    ),
    url(
        r'^loginredirect$',
        registration_views.login_redirect
    ),
    url(
        r'^logoutredirect$',
        registration_views.logout_redirect
    )
)


urlpatterns += staticfiles_urlpatterns()
