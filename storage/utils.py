#!/usr/bin/env python
# coding=utf-8

import datetime
import const 
from storage.models import *
from storage.forms import *
from purchasing.models import *
from django.db.models import Q
def get_weld_filter(model_type,dict,replace_dic=None,is_show_all = True):
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
        if replace_dic != None and replace_dic.has_key(key):
            key = replace_dic[key]
        dict_tmp[key] = val
        q = (val and Q(**dict_tmp)) or None
        filter_list.append(q)
    
    qset = filter(lambda x : x!= None ,filter_list)
    if qset:
        qset = reduce(lambda x,y:x & y ,qset)
        res_set = model_type.objects.filter(qset)
    else:
        if is_show_all:
            res_set = model_type.objects.all()
        else:
            res_set = model_type.objects.filter(id = -1)#为了获取空集合
    return res_set


def weldStoreItemsCreate(entry):
    entry_items = entry.weldmaterialentryitems_set.all()
    queryset = []
    for item in entry_items:
        try:
            storeitem = WeldStoreList(entry_item = item , count = item.total_weight,)        
            if item.material.name == u"焊条" or item.material.name == u"焊剂":
                production_date = item.production_date
                storeitem.deadline = production_date.replace(production_date.year + 2)
            queryset.append(storeitem)
        except Exception,e:
            print e
    WeldStoreList.objects.bulk_create(queryset)

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

def updateStorageLits(items_setp_StorageModel):
    isOk = True
    exist_items = []
    for item in items_set:
        try:
            print item
            storageItem = _StorageModel.objects.get(specification = item.specification)
            if storageItem.number >= item.number:
                storageItem.number -= item.number
                exist_items.append(storageItem)
            else:
                isOk = False
                break
        except Exception,e:
            print "------errors----------"
            isOk = False
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
        if categories in WELD_TYPE_LIST:
            return "WELD"
        if categories in PURCHASED_TYPE_LIST:
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
    return DB_MAP[db_type]

def getDbMap(sorce):
    weld_tuple = (WeldStoreList,WeldMaterialSearchForm,WeldingMaterialApplyCard)
    steel_tuple = (SteelMaterialStoreList,SteelMaterialSearchForm,SteelMaterialApplyCard)
    outside_tuple = (OutsideStorageList,OutsideMaterialSearchForm,OutsideApplyCard)
    auxiliarytool_tuple = (AuxiliaryToolStoreList,AuxiliaryToolMaterialSearchForm,AuxiliaryToolApplyCard)
    DB_MAP = {"weld":weld_tuple,"steel":steel_tuple,"outside":outside_tuple,"auxiliarytool":auxiliarytool_tuple}
    return DB_MAP

def modify_weld_item_status(items):
    filter_items = []
    for item in items:
        if item.inventory_count <= 0:
            item.item_status = ITEM_STATUS_SPENT
        if item.deadline != None and item. deadline < datetime.date.today():
            item.item_status = ITEM_STATUS_OVERDUE
        item.save()
        if item.item_status == ITEM_STATUS_NORMAL:
            filter_items.append(item)
    return filter_items

def gen_replace_dic(dict,fk_model = None):
    replace_dic = {}
    for k,v in dict.items():
        if "create_time" in k or "work_order" in k:
            continue
        if fk_model:
            replace_dic[k] = fk_model+"__"+k+"__contains"
        else:
            replace_dic[k] = k+"__contains"
    return replace_dic

def createAuxiliaryToolStoreList(entry):
    """
    辅助工具入库单台账更新
    """
    queryset = []
    for item in entry.auxiliarytoolentryitems_set.all():
        queryset.append(AuxiliaryToolStoreList(entry_item = item , count = item.count))
    AuxiliaryToolStoreList.objects.bulk_create(queryset)

def createSteelMaterialStoreList(entry):
    queryset = []
    for item in entry.steelmaterialentryitems_set.all():
        queryset.append(SteelMaterialStoreList(entry_item=item,specification=item.specification , steel_type=entry.steel_type ,count=item.count,length=item.length,weight=item.weight,))
    SteelMaterialStoreList.objects.bulk_create(queryset)

def getAccountDataDict(card_type):
    """
    return: model_type,form_type,account_table_path
    """
    account_table_path = "storage/accountsearch/"+card_type+".html"
    weldentry = (WeldMaterialEntryItems,WeldEntryAccountSearchForm)
    weldapply = (WeldingMaterialApplyCard,WeldApplyAccountSearchForm)
    weldstorage = (WeldStoreList,WeldStorageSearchForm)
    steelentry = (SteelMaterialEntryItems,SteelEntryAccountSearchForm)
    steelapply = (SteelMaterialApplyCardItems,SteelApplyAccountSearchForm)
    steelstorage = (SteelMaterialStoreList,SteelStorageAccountSearchForm)
    outsideentry = (OutsideStandardItems,OutsideEntryAccountSearchForm)
    outsideapply = (OutsideApplyCardItems,OutsideApplyAccountSearchForm)
    outsidestorage = (OutsideStorageList,OutsideStorageAccountSearchForm)
    auxiliarytoolentry = (AuxiliaryToolEntryItems,AuxiliaryToolEntryAccountSearchForm)
    auxiliarytoolapply = (AuxiliaryToolApplyCard,AuxiliaryToolApplyAccountSearchForm)
    auxiliarytoolstorage = (AuxiliaryToolStoreList,AuxiliaryToolStorageAccountSearchForm)

    model_dict = {"weldentry":weldentry,"weldapply":weldapply,"weldstorage":weldstorage,"steelentry":steelentry,'steelapply':steelapply,"steelstorage":steelstorage,"outsideentry":outsideentry,"outsideapply":outsideapply,"outsidestorage":outsidestorage,"auxiliarytoolentry":auxiliarytoolentry,"auxiliarytoolapply":auxiliarytoolapply,"auxiliarytoolstorage":auxiliarytoolstorage}
    return model_dict[card_type][0],model_dict[card_type][1],account_table_path

def getAccountItemDataDict(role):
    ModelTypeDict = {"weld":WeldStoreList,"auxiliarytool":AuxiliaryToolStoreList,"steel":SteelMaterialStoreList,"outside":OutsideStorageList,"auxiliarytool":AuxiliaryToolStoreList}
    AccountItemFormDict = {"weld":WeldAccountItemForm,'steel':SteelAccountItemForm,"outside":OutsideAccountItemForm,"auxiliarytool":AuxiliaryToolAccountItemForm}
    return ModelTypeDict[role],AccountItemFormDict[role]

def getApplyDataDict(apply_type):
    search_table_path = "storage/searchmaterial/store_"+apply_type+"_items_table.html"
    weld = (WeldStoreList,WeldMaterialSearchForm,WeldingMaterialApplyCard,WeldingMaterialApplyCard,WeldApplyKeeperForm)
    steel = (SteelMaterialStoreList,SteelMaterialSearchForm,SteelMaterialApplyCard,SteelMaterialApplyCardItems,None)
    outside = (OutsideStorageList,OutsideMaterialSearchForm,OutsideApplyCard,OutsideApplyCardItems,None)
    auxiliarytool = (AuxiliaryToolStoreList,AuxiliaryToolMaterialSearchForm,AuxiliaryToolApplyCard,AuxiliaryToolApplyCard,AuxiliaryToolsApplyItemForm)
    model_dict = {"weld":weld,"steel":steel,"outside":outside,"auxiliarytool":auxiliarytool}
    return model_dict[apply_type][0],model_dict[apply_type][1],model_dict[apply_type][2],model_dict[apply_type][3],model_dict[apply_type][4],search_table_path


