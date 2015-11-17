from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.conf.urls.defaults import *
from techdata import views as techdata_views

urlpatterns=patterns('',
    url(
        r'^techPreparationPlan$',
        techdata_views.techPreparationPlanViews,
    ),
    url(
        r'^processExamination$',
        techdata_views.processExaminationViews,
    ),
    url(
        r'^techFileDirectory$',
        techdata_views.techFileDirectoryViews,
    ),
    url(
        r'^firstFeeding$',
        techdata_views.firstFeedingViews,
    ),
    url(
        r'^principalMaterial$',
        techdata_views.principalMaterialViews,
    ),
    url(

        r'^weldList',
        techdata_views.weldListViews,

    ),
    url(

        r'^weldEdit',
        techdata_views.weldEditViews,

    ),
    url(

        r'^programmeEdit',
        techdata_views.programmeEditViews,

    ),
)
