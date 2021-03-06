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
        r'^bidTracking/(?P<bid_id>\w+)/$',
        purchasing_views.bidTrackingViews,
    ),
   url( 
        r'^arrivalInspection$',
        purchasing_views.arrivalInspectionViews,
    ),
   url(
        r'^arrivalInspectionConfirm/(?P<entry_typeid>\d+)/(?P<eid>\d+)/$',
        purchasing_views.arrivalInspectionConfirmViews,
    ),
    url(
        r'^arrivalCheck/(?P<bid>\w+)/$',purchasing_views.arrivalCheckViews,name='arrivalCheck',                    
    ),
    url(
        r'^inventoryTable/', 
        purchasing_views.inventoryTableViews,  
    ),
    url(
        r'^materialEntry/(?P<bid>\w+)/$',purchasing_views.materialEntryViews, name="mat_entry",                   
    ),
    url(
        r'^subApplyHome/$',purchasing_views.subApplyHomeViews,                     
    ),
    url(
        r'^subApply/(?P<sid>\w+)/$',purchasing_views.subApplyViews                     
    ),
    url(
        r'^subApplyReview/(?P<sid>\w+)/$',purchasing_views.subApplyReviewViews                     
    ),
    url(
        r'^orderFormManage$',
        purchasing_views.orderFormManageViews,
    ),
    url(
        r'^orderForm/',
        purchasing_views.orderFormViews,
    ),
    url(
        r'^processfollowing/(?P<bid>\w+)$',
        purchasing_views.processFollowingViews,
       ),
    url(
        r'^materielExecute$', purchasing_views.materielExecuteViews,
    ),
    url(
        r'^processfollowingadd$',
        purchasing_views.processFollowAdd,
     ),
    url(
        r'^materielExecuteDetail/(\d+)/(\d+)/(\d+)?$',
        purchasing_views.materielExecuteDetailViews,
    ),
    url(
        r'^statusChangeHome$',
        purchasing_views.statusChangeViews,
    ),
    url(
        r'^statusChangeHistory/(?P<bid>\w+)/$',
        purchasing_views.statusChangeHistoryViews,name="statuschange_history",
    ),
    url(
        r'^statusChange/(?P<bid>\w+)/$',
        purchasing_views.statusChangeApplyViews,name="statuschange",
       ),
    url(
        r'^bidformapprove$',
        purchasing_views.bidformApproveViews,
    ),
    url(
        r'^bidformapproveid/(?P<bid>\w+)/$',
        purchasing_views.bidformApproveIDViews,
    ),
    url(
        r'^contractFinance/$',
        purchasing_views.contractFinanceViews,
    ),
    url(
        r'^bidapplyform/(?P<bid>\w+)/$',
        purchasing_views.bidApplyFormViews,
    ),
    url(
        r'^suppliercheck/(?P<bid>\w+)/$',
        purchasing_views.SupplierCheckViews,
    ),
    url(
        r'^qualitycard/(?P<bid>\w+)/$',
        purchasing_views.QualityCardViews,
    )
)
