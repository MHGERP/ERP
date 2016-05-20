#coding=UTF-8
from models import *

from django.contrib import admin

Registers = (
    WeldingMaterialApplyCard,
    StoreRoom,
    WeldingMaterialHumitureRecord,
    WeldingMaterialBakeRecord,
    WeldRefund,
    AuxiliaryToolStoreList,
    AuxiliaryToolApplyCard,
    AuxiliaryToolEntry,
    AuxiliaryToolEntryItems,
    WeldMaterialEntry,
    WeldMaterialEntryItems,
    WeldStoreList,
    WeldStoreThread,
    OutsideStandardEntry,
    OutsideStandardItems,
    OutsideStorageList,
    OutsideApplyCard,
    OutsideApplyCardItems,
    OutsideRefundCard,
    OutsideRefundCardItems,
    SteelMaterialEntry,
    SteelMaterialEntryItems,
    SteelMaterialStoreList,
    SteelMaterialApplyCard,
    SteelMaterialApplyCardItems,
    SteelMaterialRefundCard,
    BarSteelMaterialRefundItems,
    BoardSteelMaterialRefundItems,
    CardStatusStopRecord,
)

for reg in Registers:
    admin.site.register(reg)
