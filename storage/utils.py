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
        storeitem = WeldStoreList(entry_time = item.entry.entry_time,specification=item.material.specification,material_id=item.material.material.material_id,count=item.material.count,entry_item = item)
        storeitem.save()

def storeConsume(applycard):
    specification = applycard.standard
    material_id = applycard.material_number
    consume_count = applycard.actual_quantity
    avail_items = WeldStoreList.objects.filter(material_id=material_id,specification = specification).order_by("entry_time")
    for item in avail_items:
        if consume_count <= item.count:
            item.count -= consume_count
            item.save()
            break
        else:
            consume_count -= item.count
            item.count = 0
            item.save()
    
