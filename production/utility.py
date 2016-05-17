#!/usr/bin/env python
# coding=utf-8
from const import *
from const.models import *
from storage.models import *
from production.models import *
import datetime

ApplyCardModelDICT = {
    SteelMaterialApplyCard:1,
    AuxiliaryToolApplyCard:2,
    OutsideApplyCard:3,
    WeldingMaterialApplyCard:4
}

def get_applycard_code(ApplyCardModel):
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    num = ApplyCardModel.objects.filter(applycard_code__startswith=date_str).count() + 1
    return "%s%d%04d" % (date_str, ApplyCardModelDICT[ApplyCardModel], num)
