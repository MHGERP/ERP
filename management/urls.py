from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.conf.urls.defaults import *
from management import views as management_views
urlpatterns=patterns('',
    url(
        r'^$',
        management_views.userManagementViews,
    ),
    url(
        r'^userManagement$',
        management_views.userManagementViews,
    ),
    url(
        r'^groupManagement$',
        management_views.groupManagementViews,
    ),
    url(
        r'^titleManagement$',
        management_views.titleManagementViews,
    ),
    url(
        r'^messageManagement$',
        management_views.messageManagementViews,
    ),
    url(
        r'^authorityManagement$',
        management_views.authorityManagementViews,
    ),
    url(
        r'^newsRelease$',
        management_views.newsReleaseViews,
    ),
)
