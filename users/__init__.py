#coding: UTF-8

import operator

PENDING_ORDER = "pendingOrder"
PURCHASING_AUTHORITY = (
    (PENDING_ORDER, u"待处理工作令"),
)


STORAGE_KEEPER = "storage_keeper"
STORAGE_AUTHORITY = (
    (STORAGE_KEEPER,u"库管员权"),
)

AUTHORITY_SET = reduce(operator.add, (PURCHASING_AUTHORITY, STORAGE_AUTHORITY))

