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
    PurchasingEntry,
    PurchasingEntryItems,
    MaterielPurchasingStatus,
    SupplierSelect,
    MaterialSubApply,
    MaterialSubApplyItems,
    ProcessFollowingInfo,
)

for item in RegisterClass:
    admin.site.register(item)
