#coding: UTF-8

import operator

PENDING_ORDER = "pendingOrder"
PURCHASING_AUTHORITY = (
    (PENDING_ORDER, u"待处理工作令"),
)



STORAGE_AUTHORITY = (

)

AUTHORITY_SET = reduce(operator.add, (PURCHASING_AUTHORITY, STORAGE_AUTHORITY))

