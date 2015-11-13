#coding=UTF-8

from django.contrib import admin
from models import *

Registers = (
    WeldingMaterialApplyCard,
    StoreRoom,
    WeldingMaterialHumitureRecord,
    SteelMaterialPurchasingEntry,
    SteelMaterial,
    BoardSteelMaterialLedger,
    BarSteelMaterialLedger,
    CommonSteelMaterialReturnCardInfo,
    BoardSteelMaterialReturnCardContent,
    BarSteelMaterialReturnCardContent
)

for reg in Registers:
    admin.site.register(reg)
