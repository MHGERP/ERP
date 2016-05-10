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
    OutsideStandardItem,
    OutsideStorageList,
    OutsideApplyCard,
    OutsideApplyCardItem,
    SteelMaterialEntry,
    SteelMaterialEntryItems,
    SteelMaterialStoreList,
    SteelMaterialApplyCard,
    SteelMaterialApplyCardItems,
)

for reg in Registers:
    admin.site.register(reg)
