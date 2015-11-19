from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.conf.urls.defaults import *
from production import views as production_views

urlpatterns=patterns('',
    url(
        r'^task_allocation$',
        production_views.taskAllocationViews,
    ),
    url(
        r'^task_confirm$',
        production_views.taskConfirmViews,
    ),
    url(
        r'^materiel_use$',
        production_views.materielUseViews,
    )

)
