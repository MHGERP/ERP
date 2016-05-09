#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from production.models  import *

RegisterClass = (
    SynthesizeFileListStatus,
    ProductionPlan,
    ProductionWorkGroup,
    ProcessDetail,
)

for item in RegisterClass:
    admin.site.register(item)

class ProductionUserAdmin(admin.ModelAdmin):
    search_fields = ['production_user_id__username']

RegisterSearchClass = (
    (ProductionUser,ProductionUserAdmin),
)

for temp in RegisterSearchClass:
    admin.site.register(temp[0],temp[1])