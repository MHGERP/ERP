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
     url(
        r'product_bidFile_add$',
         sell_views.product_bidFile_add,
    ),
    url(
        r'^bidFile_to_manufacture$',
        sell_views.bidFile_to_manufacture,
    ),
    url(
        r'^bidFile_to_techdata$',
        sell_views.bidFile_to_techdata,
    ),
    url(
        r'^bidFile_to_purchasing$',
        sell_views.bidFile_to_purchasing,
    ),
)
