from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.conf.urls.defaults import *
from purchasing import views as purchasing_views
urlpatterns=patterns('',
    url(
        r'^purchasingfollowing$',
        purchasing_views.purchasingFollowingViews,
    ),
    url(
        r'^pendingOrder$',
        purchasing_views.pendingOrderViews,
    ),
    url(
        r'^arrivalInspection$',
        purchasing_views.arrivalInspectionViews,
    ),
    url(
        r'arrivalCheck/(?P<bid>\w+)/$',purchasing_views.arrivalCheckViews,name='arrivalCheck',                    
    )
)
