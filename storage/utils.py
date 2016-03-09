#!/usr/bin/env python
# coding=utf-8

import datetime
import const 
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
        res_set = model_type.objects.all().order_by('-id')
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
    """
    author:shenlian
    func:entry obj for entry save form and items
    """
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
    """
    Author: Shen Lian
    Func:redict url by request param
    """
    redict_path = request.GET.get("redict_path",None)
    if redict_path:
        entry_url = redict_path
    return entry_url

class HandleEntry(object):
    def getEntry(self,user,bidform):
        pass
    def getEntryItem(self,materiel,entry):
        pass
    def saveEntry(self,items,user,bidform):
        entry_obj = self.getEntry(user,bidform)
        entry_obj.save()
        for item in items:
            entryitem_obj = self.getEntryItem(item.material,entry_obj)
            entryitem_obj.save()
            item.check_pass = True
            item.save()

class HandleEntryWeld(HandleEntry):
    def getEntry(self,user,bidform):
        return WeldMaterialEntry(purchaser = user , bidform = bidform , entry_status = STORAGESTATUS_PURCHASER)
    def getEntryItem(self,materiel,entry):
        return WeldMaterialEntryItems(material = materiel,entry = entry)

class HandleEntryPurchased(HandleEntry):
    def getEntry(self,user,bidform):
        return OutsideStandardEntry(purchaser = user,entry_status = STORAGESTATUS_PURCHASER,bidform = bidform)
    def getEntryItem(self,materiel,entry):
        return OutsideStandardItem(materiel = materiel,entry = entry,schematic_index=materiel.schematic_index,specification = materiel.specification,number = materiel.count,unit = materiel.unit )

class HandleEntrySteel(HandleEntry):
    def getEntry(self,user,bidform):
        pass
    def getEntryItem(self,materiel,entry):
        pass

from itertools import *
class AutoGenEntry(object):
    Entry_DICT = {"WELD":HandleEntryWeld,"PURCHASED":HandleEntryPurchased}
    def key_cmp_func(self,it):
        categories = it.material.material.categories
        if categories in self.WELD_TYPE_LIST:
            return "WELD"
        if categories in self.PURCHASED_TYPE_LIST:
            return "PURCHASED"
    
    def group_by(self):
        sorted_items_set = sorted(self.items_set,key=self.key_cmp_func)
        item_groupby_dict = {}
        for label,items in groupby(sorted_items_set,key=self.key_cmp_func):
            item_groupby_dict[label]=list(items)
        return item_groupby_dict

    def processEntry(self,groupby_items):
        for k,v in groupby_items.items():
            handle = self.Entry_DICT[k]()
            handle.saveEntry(v,self.user,self.bidform)

    def __init__(self,user,items_set,bidform):
        self.user = user
        self.items_set = items_set
        self.bidform = bidform
        groupby_items = self.group_by()
        self.processEntry(groupby_items)


def checkStorage(db_type,sorce=None):
    DB_MAP = getDbMap(sorce)
    db_model = DB_MAP[db_type]
    return db_model

def getDbMap(sorce):
    DB_MAP = {WELD:WeldStoreList,PROFILE:BarSteelMaterialLedger,SHEET:BoardSteelMaterialLedger,PURCHASED:OutsideStorageList,AUXILIARY_TOOL:AuxiliaryTool}
    if sorce == "purchaser":    
        for tp in WELD_TYPE_LIST:
            if tp in WELD_TYPE_LIST:
                DB_MAP[tp] = WeldStoreList
    return DB_MAP
