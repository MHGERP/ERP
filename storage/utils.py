#!/usr/bin/env python
# coding=utf-8

import datetime
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
        print qset
        qset = reduce(lambda x,y:x & y ,qset)
        res_set = model_type.objects.filter(qset)
    else:
        res_set = model_type.objects.all()
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
   
def get_today(timetype=""):
    """
    timetype : String year,month,day
    """
    return getattr(datetime.date.today(),timetype) if timetype != "" else datetime.date.today()

def getRequestByMethod(request):
    if request.method == "GET":
        return request.GET,"GET"
    else:
        return request.POST,"POST"

def saveEntry(obj,role,user,status):
    """
    author:shenlian
    func:save entry,change each role and status
    params: role is a string
    """
    setattr(obj,role,user)
    obj.entry_status = status
    obj.save()

class EntryObject(object):
    context = {}
    flag = False
    def __init__(self,status_list,_Model,eid):
        self.status_list = status_list
        self._Model = _Model
    def save_entry(self,entry_obj,role,user,form_list):
        if self.save_form(form_list):
            entry_status = entry_obj.entry_status
            index = self.status_list.index(entry_status)
            if entry_status != self.status_list[-1]:
                index += 1
                entry_obj.entry_status = self.status_list[index]
                setattr(entry_obj,role,user)
                entry_obj.save()
        self.context["entry_obj"] = entry_obj
        return self.context
    
    def checkShow(self,entry_obj,entry_status):
        return entry_obj. entry_status == entry_status
    
    def save_form(self,form_list):
        flag = True
        for form in form_list:
            if not form[1].is_valid():
                flag = False
            self.context[form[0]] = form[1] 
        if flag:
            for form in form_list:
                form[1].save()
        self.flag = flag
        return flag

def saveRolers(obj,role,user,status = None):
    """
    author:shenlian
    func:save entry,change each role and status
    params: role is a string
    """
    setattr(obj,role,user)
    if status != None:
        obj.entry_status = status
    obj.save()

def setObjAttr(obj,field,value):
    setattr(obj,field,value)
    obj.save()

def updateStorageLits(items_set,_StorageModel):
    isOk = True
    exist_items = []
    for item in items_set:
        try:
            storageItem = _StorageModel.objects.get(specification = item.specification)
            if storageItem.number >= item.number:
                storageItem.number -= item.number
                exist_items.append(storageItem)
            else:
                isOk = False
                break
        except Exception,e:
            print e
    if isOk:
        for item in exist_items:
            item.save()
    return isOk


def getUrlByViewMode(request,entry_url):
    redict_path = request.GET.get("redict_path",None)
    if redict_path:
        entry_url = redict_path
    return entry_url
