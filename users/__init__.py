#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-07-26 11:13
# Last modified: 2016-09-11 13:15
# Filename: __init__.py
# Description:

import operator
from users.models import GlobalPermission

PENDING_ORDER = "pendingOrder"
TECH_FILE_DIRECTORY = "techFileDirectory"
DESIGN_BOM = "designBOM"
PROCESS_BOM = "processBOM"
TRANSFER_CARD_EDIT = "transferCardEdit"
WELD_LIST = "weldList"
TECH_HOT_DEEL = "techHotDeel"

PURCHASING_AUTHORITY = (
    (PENDING_ORDER, u"待处理工作令"),
    (TECH_FILE_DIRECTORY, u"工艺技术文件目录"),
    (DESIGN_BOM, u"设计库"),
    (PROCESS_BOM, u"工艺库"),
    (TRANSFER_CARD_EDIT, u"流转卡编辑"),
    (WELD_LIST, u"焊缝表"),
    (TECH_HOT_DEEL, u"热处理列表"),
)


STORAGE_KEEPER = "storage_keeper"
STORAGE_AUTHORITY = (
    (STORAGE_KEEPER,u"库管员权"),
)

AUTHORITY_SET = reduce(operator.add, (PURCHASING_AUTHORITY, STORAGE_AUTHORITY))

# view_storage, created = GlobalPermission.objects.get_or_create(codename='view_storage', name=u'')
# view_storage.save()
