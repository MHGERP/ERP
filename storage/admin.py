#coding=UTF-8

from django.contrib import admin
from storage.models import *

Registers = (
    WeldingMaterialApplyCard,
    StoreRoom,
    WeldingMaterialHumitureRecord,
    WeldingMaterialBakeRecord,
    WeldRefund,
)

for reg in Registers:
    admin.site.register(reg)
