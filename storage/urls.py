#!/usr/bin/env python
# coding=utf-8
from django.conf.urls import patterns, include, url
from storage import views as storage_views

urlpatterns = patterns('',
    url(
        r'^weldmaterialhome$',
        storage_views.weldMaterialHomeViews,
    ),
    url(
        r'^weldentryhome$',
        storage_views.weldEntryHomeViews,
    ),
    url(
        r'^weldentryconfirm/(?P<eid>\w+)$',
        storage_views.weldEntryConfirmViews,
    ),
)


