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
    url(
        r'^weldapply$',
        storage_views.Weld_Apply_Card_List,
    ),
    url(
        r'weldapply/detail$',
        storage_views.Weld_Apply_Card_Detail,
    ),
    url(
        r'weldapply/submit$',
        storage_views.Handle_Apply_Card_Form,
    ),
    url(
        r'^weldhumiture$',
        storage_views.weldHumitureHomeViews,
    ),
    url(
        r'^weldhumDetail/(?P<eid>\w+)$',
        storage_views.weldhumDetail,
    ),
    url( 
        r'^weldhumNewRecord$',
        storage_views.weldhumNewRecord,
    ),
)


