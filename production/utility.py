#!/usr/bin/env python
# coding=utf-8
from const import *
from const.models import *
from storage.models import *
from production.models import *
from production import *
import datetime
ApplyCardModelDICT = {
    SteelMaterialApplyCard:"G",
    AuxiliaryToolApplyCard:"F",
    OutsideApplyCard:"W",
    WeldingMaterialApplyCard:"H",
}

ApplyCardModelCheckDICT = {
}
for k,v in ApplyCardModelDICT.items():
    ApplyCardModelCheckDICT[v]=k

def get_applycard_code(ApplyCardModel):
    date_str = ApplyCardModelDICT[ApplyCardModel] + datetime.datetime.now().strftime("%Y%m%d")
    num = ApplyCardModel.objects.filter(applycard_code__startswith=date_str).count() + 1
    return "%s%04d" % (date_str, num)
