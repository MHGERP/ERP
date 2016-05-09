#!/usr/bin/env python
# coding=utf-8
from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.conf.urls.defaults import *
from sell import views as sell_views

urlpatterns=patterns('',
    url(
        r'^productions$',
        sell_views.productionsView,
    ),
)
