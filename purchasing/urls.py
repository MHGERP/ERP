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
        r'^materialSummarize$',
        purchasing_views.materialSummarizeViews,
    ),
    url(
        r'^selectsupplier/(?P<bid>\w+)$',
        purchasing_views.selectSupplierViews,
    ),
    url(
            r'^suppliermanagement$',
            purchasing_views.supplierManagementViews,
        ),
    url(
            r'^bidTracking$',
            purchasing_views.bidTrackingViews,
        ),
    url(
        r'^suppliermanagement$',
        purchasing_views.supplierManagementViews,
    ),
    url(
        r'^bidTracking$',
        purchasing_views.bidTrackingViews,
    ),
   url( 
        r'^arrivalInspection$',
        purchasing_views.arrivalInspectionViews,
    ),
    url(
        r'^arrivalCheck/(?P<bid>\w+)/$',purchasing_views.arrivalCheckViews,name='arrivalCheck',                    
    ),
    url(
        r'^inventoryTable/', 
        purchasing_views.inventoryTableViews,  
    ),
    url(
        r'^materialEntry$',purchasing_views.materialEntryViews,                     
    ),
    url(
        r'^subApply$',purchasing_views.subApplyViews,                     
    ),
    url(
        r'^materielExecute$', purchasing_views.materielExecuteViews,
    ),
)
