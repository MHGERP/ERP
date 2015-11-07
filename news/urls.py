from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

from django.conf.urls.defaults import *
from news import views as news_views

urlpatterns=patterns('',
    url(
        r'^newslist/(?P<news_id>\d+)$',
        news_views.read_news,
        name = 'read_news'
    ),
    url(
    	r'^newslist/news_cate=(?P<news_cate>\S+)$',
    	news_views.list_news_by_cate,
    	name = 'newslist_cate'
    )
)
