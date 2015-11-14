from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.conf.urls.defaults import *
from techdata import views as techdata_views

urlpatterns=patterns('',
    url(
        r'^techPreparationPlan$',
        techdata_views.techPreparationPlanViews,
    ),
)
