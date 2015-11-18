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
        r'^synthesize_filelist$',
        production_views.synthesizeFileListViews,
    ),
    url(
    	r'^man_hour_summarize$',
    	production_views.man_hour_summarizeViews,
    ),
)
