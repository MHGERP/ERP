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
        r'^weldapply$',
        storage_views.Weld_Apply_Card_List,
    ),
    url(
        r'weldapply/detail$',
        storage_views.Weld_Apply_Card_Detail,
    ),
)


