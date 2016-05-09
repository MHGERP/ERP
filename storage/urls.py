#!/usr/bin/env python
# coding=utf-8
from django.conf.urls import patterns, include, url
from storage import views as storage_views
from django.views.generic.simple import direct_to_template
urlpatterns = patterns('',
    url(
        r'^weldmaterialhome$',
        storage_views.weldMaterialHomeViews,
    ),
    url(
        r'^steelrefunddetail/(?P<typeid>\d+)/(?P<rid>\d+)$',
        storage_views.steelrefunddetailViews,
    ),
    url(
        r'^steelrefund$',
        storage_views.steelRefundViews,
    ),
    url(
        r'^steelmaterialhome$',
        storage_views.steelMaterialHomeViews,
    ),
    url(
        r'^steelapply$',
        storage_views.steelApplyViews,
    ),
    url(
        r'^steelapplydetail/(?P<typeid>\d+)/(?P<rid>\d+)$',
        storage_views.steelApplyDetailViews,
    ),
    url(
        r'^steelledger$',
        storage_views.steelLedgerViews,
    ),
    url(
        r'^weldentryhome$',
        storage_views.weldEntryHomeViews,
    ),
    url(
        r'^steelentryhome$',
        storage_views.steelEntryHomeViews,
    ),
    url(
        r'^weldentryconfirm/(?P<eid>\w+)$',
        storage_views.weldEntryConfirmViews,
    ),
    url(
        r'^steelentryconfirm/(?P<eid>\d+)$',
        storage_views.steelEntryConfirmViews,
    ),
    url(
        r'^weldapply$',
        storage_views.Weld_Apply_Card_List,
    ),
    url(
        r'weldapply/detail$',
        storage_views.Weld_Apply_Card_Detail,
    ),
    url(
        r'weldapply/submit$',
        storage_views.Handle_Apply_Card_Form,
    ),
    url(
        r'^weldhumiture$',
        storage_views.weldHumitureHomeViews,
    ),
    url(
        r'^weldhumDetail/(?P<eid>\w+)$',
        storage_views.weldhumDetail,
    ),
    url( 
        r'^weldhumNewRecord$',
        storage_views.weldhumNewRecord,
    ),
    url(
        r'^weldbake$',
        storage_views.weldbakeHomeViews,
    ),
    url(
        r'^weldrefund$',
        storage_views.weldRefundViews,
    ),
    url(
        r'^weldbakeDetail/$',
        storage_views.weldbakeDetail,
    ),
    url( 
        r'^weldbakeNewRecord$',
        storage_views.weldbakeNewRecord,
    ),
    url(
        r'^weldapplyrefund$',
        storage_views.weldapplyrefundHomeViews,
    ),
    url(
        r'^weldapplyrefundDetail/(?P<index>\w+)$',
        storage_views.weldapplyrefundDetail,
    ),


    url( 
        r'^weldrefunddetail/(?P<rid>\w+)$',
        storage_views.weldRefundDetailViews,
    ),
    url(
        r'^auxiliarytools$',
        storage_views.AuxiliaryToolsHomeView,
    ),
    url(
        r'^auxiliarytools/apply$',
        storage_views.AuxiliaryToolsApplyView,
    ),
    url(
        r'^auxiliarytools/applylist$',
        storage_views.AuxiliaryToolsApplyListView,
    ),

    url(
        r'^auxiliarytools/ledger$',
        storage_views.AuxiliaryToolsLedgerView,
    ),
    url(
        r'^auxiliarytools/ledger/entry$',
        storage_views.AuxiliaryToolsLedgerEntryView,
    ),
    url(
        r'^auxiliarytools/ledger/apply$',
        storage_views.AuxiliaryToolsLedgerApplyView,
    ),
    url(
        r'^auxiliarytools/ledger/inventory$',
        storage_views.AuxiliaryToolsLedgerInventoryView,
    ),
    url(
        r'^auxiliarytools/warehousedetail$',
        storage_views.AuxiliaryToolsEntryApplyDetailView,
    ),
    url(
        r'^auxiliarytools/entry$',
        storage_views.AuxiliaryToolsEntryView,
    ),
    url(
        r'^auxiliarytools/entrylist$',
        storage_views.AuxiliaryToolsEntryListView,
    ),
    url(
        r'^auxiliarytools/ledger/entry/entry_card$',
        storage_views.AuxiliaryToolsLedgerEntryCardView,
    ),
    url(
        r'^auxiliarytools/ledger/apply/apply_card$',
        storage_views.AuxiliaryToolsLedgerApplyCardView,
    ),
    url(
        r'^auxiliarytools/entry_apply_detail$',
        storage_views.AuxiliaryToolsEntryApplyDetailView,
    ),
    url(
        r'^weldaccounthome$',
        storage_views.weldAccountHomeViews,
    ),
    url(
        r'^weldentryaccount$',
        storage_views.weldEntryAccountViews,
    ),   
    url(
        r'^weldapplyaccount$',
        storage_views.weldApplyAccountViews,
    ),   
    url(
        r'^weldstorageaccount$',
        storage_views.weldStorageAccountHomeViews,
    ),
    url(
        r'^outsidehome$',
        storage_views.outsideHomeViews,
    ),
    url(
        r'^outside/entryhome$',
        storage_views.outsideEntryHomeViews,    
    ),
    url(
        r'^outside/entryconfirm/(?P<eid>\w+)$',
        storage_views.outsideEntryConfirmViews,    
    ),
    url(
        r'^storethread$',
        storage_views.StoreThreadViews,
    ),
    url(
        r'^outside/applycardhome$',
        storage_views.outsideApplyCardHomeViews,    
    ),
    url(
        r'^outside/applycardconfirm/(?P<cid>\w+)$',
        storage_views.outsideApplyCardConfirmViews,    
    ),
    url(
        r'^outside/account/home$',
        storage_views.outsideAccountHomeViews,    
    ),
    url(
        r'^outside/outsidestorageaccount$',
        storage_views.outsideStorageAccountViews,
       ),
    url(
        r'^outside/account/entryhome$',
        storage_views.outsideEntryAccountHomeViews,name="outside_account_entryhome"
    ),
    url(
        r'^outside/account/applycardhome$',
        storage_views.outsideApplyCardAccountHomeViews,name="outside_account_applycardhome"
    ),
    url(
        r'^basedatamanage$',direct_to_template,{"template":"storage/basedata/basedatahome.html"}
    ),
    url(
        r'^storeroommanage$',
        storage_views.storeRoomManageViews,
    ),
)
