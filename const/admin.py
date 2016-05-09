#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from const.models  import *

RegisterClass = (
    OrderFormStatus,
    BidFormStatus,
    WorkOrder,
    SubWorkOrder,
    InventoryType,
    Materiel,
    Material,
    ImplementClassChoices,
)
for item in RegisterClass:
    admin.site.register(item)
