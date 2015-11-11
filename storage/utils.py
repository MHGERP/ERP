#!/usr/bin/env python
# coding=utf-8

from storage.models import *
from purchasing.models import *
from django.db.models import Q

def get_filter(date,purchaser,work_order):
    if purchaser == "-1":
        purchaser = ""
    q1 = (date and Q(entry_time = date)) or None
    q2 = (purchaser and Q(purchaser = purchaser)) or None
    q3 = (work_order and Q(work_order = work_order)) or None
    qset = filter(lambda x : x!= None ,[q1,q2,q3])
    return qset
