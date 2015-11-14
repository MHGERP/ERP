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

        r'^steelmaterialhome$',
        storage_views.steelMaterialHomeViews,
    ),
    url(
        r'^weldentryhome$',
        storage_views.weldEntryHomeViews,
    ),
    url(
        r'^steelentryhome$',
        storage_views.steelEntryHomeViews,
    ),
    url(
        r'^weldentryconfirm/(?P<eid>\w+)$',
        storage_views.weldEntryConfirmViews,
    ),
    url(
        r'^weldapply$',
        storage_views.Weld_Apply_Card_List,
    ),
    url(
        r'weldapply/detail$',
        storage_views.Weld_Apply_Card_Detail,
    ),
)


