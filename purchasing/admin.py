#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from purchasing.models  import *

RegisterClass = (
    OrderForm,
    MaterielFormConnection,
    BidForm,
    ArrivalInspection,
    Supplier,
    SupplierFile,
    MaterielPurchasingStatus,
    SupplierSelect,
    MaterialSubApply,
    MaterialSubApplyItems,
    BidComment,
    MaterielExecute,
    ProcessFollowingInfo,
    StatusChange,
    StatusChangeReason,
    MaterielExecuteDetail,
    ContractDetail,
    MaterielCopy,
    bidApply,
    CommentStatus,
    SupplierCheck,
    qualityPriceCard,
    QuotingPrice,
    SubApplyComment
)

for item in RegisterClass:
    admin.site.register(item)
