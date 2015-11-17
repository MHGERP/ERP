
from django.conf.urls import patterns, include, url
from home import views as home_views

urlpatterns = patterns('',
    url(
        r'^$',
        home_views.homepageViews,
    ),
  

)

