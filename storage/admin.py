#coding=UTF-8

from django.contrib import admin
from models import *

Registers = (
    WeldingMaterialApplyCard,
    StoreRoom,
    WeldingMaterialHumitureRecord,
)

for reg in Registers:
    admin.site.register(reg)
