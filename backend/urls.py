'''
Created on 2013-04-07

@author: tianwei 
'''
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *

from backend.errorviews import error403, error404, error500

urlpatterns = patterns('',
    url(r'^403/$', error403),
    url(r'^500/$', error500),
    url(r'^404/$', error404),
)
