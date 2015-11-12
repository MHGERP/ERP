#coding=UTF-8

from django.contrib import admin
from storage.models import *

Registers = (
    WeldingMaterialApplyCard,
    StoreRoom,
    WeldingMaterialHumitureRecord,
    WeldRefund,
)

for reg in Registers:
    admin.site.register(reg)
