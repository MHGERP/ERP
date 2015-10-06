#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from purchasing.models  import *

RegisterClass = (
    BidForm,
    ArrivalInspection,
    Supplier,
    SupplierFile,
    PurchasingEntry,
    PurchasingEntryItems,
    MaterielPurchasingStatus,
    MaterialSubApply,
    MaterialSubApplyItems,
)

for item in RegisterClass:
    admin.site.register(item)
