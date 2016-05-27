#!/usr/bin/env python
# coding=utf-8
from const import *
from const.models import *
from storage.models import *
from production.models import *
from production import *
import datetime
CardModelDICT = {
    SteelMaterialApplyCard:"G",
    AuxiliaryToolApplyCard:"F",
    OutsideApplyCard:"W",
    WeldingMaterialApplyCard:"H",
    SteelMaterialRefundCard:"g",
    WeldRefund:"h",
    OutsideRefundCard:"w",
}

CardModelCheckDICT = {
}
for k,v in CardModelCheckDICT.items():
    CardModelCheckDICT[v]=k

def get_card_code(CardModel):
    date_str = CardModelDICT[CardModel] + datetime.datetime.now().strftime("%Y%m%d")
    try:
        num = CardModel.objects.filter(applycard_code__startswith=date_str).count() + 1
    except:
        num = CardModel.objects.filter(refund_code__startswith=date_str).count() + 1
    return "%s%04d" % (date_str, num)
