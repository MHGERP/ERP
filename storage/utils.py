#!/usr/bin/env python
# coding=utf-8

from storage.models import *
from purchasing.models import *
from django.db.models import Q

def get_weld_filter(model_type,dict):
    """
    author: Shen Lian
    summary:filter objects by search form
    params: model_type: destination Model; dict : search params;
    return: model_type set
    """
    filter_list = []
    for key,val in dict.items():
        dict_tmp = {}
        if val == "-1":
            val = ""
        dict_tmp[key] = val
        q = (val and Q(**dict_tmp)) or None
        filter_list.append(q)
    qset = filter(lambda x : x!= None ,filter_list)
    if qset:
        qset = reduce(lambda x,y:x & y ,qset)
        res_set = model_type.objects.filter(qset)
    else:
        res_set = []
    return res_set

def weldStoreItemsCreate(entry):
    weld_set = entry.weldmaterialentryitems_set.all()
    for item in weld_set:
        storeitem = WeldStoreList.objects.filter(material_id = item.material.material.material_id,specification = item.material.specification,entry_time=item.entry.entry_time)
        if storeitem.count() > 0:
            old_item = storeitem[0]
            old_item.count = old_item.count + float(item.material.count)
            old_item.save()
        else:
            storeitem = WeldStoreList(entry_time = item.entry.entry_time,specification=item.material.specification,material_id=item.material.material.material_id,count=item.material.count)
            storeitem.save()

