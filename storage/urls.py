#!/usr/bin/env python
# coding=utf-8
from django.conf.urls import patterns, include, url
from storage import views as storage_views

urlpatterns = patterns('',
    url(
        r'^$',
        storage_views.weldMaterialHomeViews,
    ),
)


