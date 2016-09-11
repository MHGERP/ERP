#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-09-11 12:24
# Last modified: 2016-09-11 12:45
# Filename: urls.py
# Description:
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
        r'^controlManagement$',
        management_views.controlManagementViews,
    ),
    url(
        r'^newsRelease$',
        management_views.newsReleaseViews,
    ),
    url(
        r'^newsManagement$',
        management_views.newsManagementViews,
    ),
    url(
        r'^titleSetting$',
        management_views.titleSettingViews,
    ),
    url(
        r'^authorityManagement$',
        management_views.authorityManagementViews,
    ),
)
