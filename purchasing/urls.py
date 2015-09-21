from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.conf.urls.defaults import *
from purchasing import views as purchasing_views
urlpatterns=patterns('',
    url(
        r'^purchasingfollowing$',
        purchasing_views.purchasingFollowingViews,
    )                    
)
