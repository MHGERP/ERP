# coding: UTF-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from purchasing.models import BidForm,ArrivalInspection,Supplier,SupplierFile,PurchasingEntry,PurchasingEntryItems,MaterialSubApplyItems,MaterialSubApply
from const import *
from const.models import Materiel
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib.auth.models import User
from django.db import transaction 
from const.models import WorkOrder, Materiel
from const.forms import InventoryTypeForm
from purchasing.forms import SupplierForm,SubApplyItemForm
from django.http import HttpResponseRedirect

@dajaxice_register
def searchPurchasingFollowing(request,bidid):
    bidform_processing=BidForm.objects.filter(bid_id=bidid)
    context={
        "bidform":bidform_processing,
        "BIDFORM_STATUS_SELECT_SUPPLIER":BIDFORM_STATUS_SELECT_SUPPLIER,
        "BIDFORM_STATUS_INVITE_BID":BIDFORM_STATUS_INVITE_BID,
        "BIDFORM_STATUS_PROCESS_FOLLOW":BIDFORM_STATUS_PROCESS_FOLLOW,
        "BIDFORM_STATUS_CHECK_STORE":BIDFORM_STATUS_CHECK_STORE 
    }
    purchasing_html=render_to_string("purchasing/purchasingfollowing/purchasing_following_table.html",context)
    data={
        'html':purchasing_html
    }
    return simplejson.dumps(data)

@dajaxice_register
def checkArrival(request,aid,cid):
    arrivalfield = ARRIVAL_CHECK_FIELDS[cid]
    cargo_obj = ArrivalInspection.objects.get(id = aid)
    val = not getattr(cargo_obj,arrivalfield)
    setattr(cargo_obj,arrivalfield,val)
    cargo_obj.save()
    val = getattr(cargo_obj,arrivalfield)
    data = {
        "flag":val, 
    }
    return simplejson.dumps(data)

@dajaxice_register
@transaction.commit_manually
def genEntry(request,bid):
    try:
        bidform = BidForm.objects.get(bid_id = bid)
        user = request.user
        purchasingentry = PurchasingEntry(bidform = bidform,purchaser=user,inspector = user , keeper = user) 
        purchasingentry.save()
    except Exception, e:
        transaction.rollback()
        print e
    flag = isAllChecked(bid,purchasingentry)
    if flag:
        transaction.commit()
    else:
        transaction.rollback()
    data = {
        'flag':flag,
    }
    return simplejson.dumps(data)

@dajaxice_register
def SupplierUpdate(request,supplier_id):
    supplier=Supplier.objects.get(pk=supplier_id)

    supplier_html=render_to_string("purchasing/supplier/supplier_file_table.html",{"supplier":supplier})
    return simplejson.dumps({'supplier_html':supplier_html})

def isAllChecked(bid,purchasingentry):
    cargo_set = ArrivalInspection.objects.filter(bidform__bid_id = bid)
    try:
        for cargo_obj in cargo_set:
            entryitem = PurchasingEntryItems(material = cargo_obj.material,purchasingentry = purchasingentry)
            for key,field in ARRIVAL_CHECK_FIELDS.items():
                val = getattr(cargo_obj,field)
                if not val:
                    return False
            entryitem.save()
    except Exception,e:
        print e
    return True

@dajaxice_register
def chooseInventorytype(request,pid):
    #pid=int(pid)
    items = Materiel.objects.filter(inventory_type__id=pid)
    inventory_list = []
    for item in items:
        if(item.materielpurchasingstatus.add_to_detail == True):
            inventory_list.append(item)
    context={
        "inventory_detail_list":inventory_list,
    }
    new_order_form_html = render_to_string("widgets/new_order_form.html",context)
    new_purchasing_form_html = render_to_string("widgets/new_purchasing_form.html",context)
    inventory_detail_html = render_to_string("widgets/inventory_detail_table.html",context)
    main_material_quota_html = render_to_string("widgets/main_material_quota.html",context)
    accessory_quota_html = render_to_string("widgets/accessory_quota.html",context)
    first_send_detail_html = render_to_string("widgets/first_send_detail.html",context)
    out_purchasing_detail_html = render_to_string("widgets/out_purchasing_detail.html",context)
    cast_detail_html = render_to_string("widgets/cast_detail.html",context)
    
    return simplejson.dumps({
        "new_order_form_html":new_order_form_html,
        "new_purchasing_form_html":new_purchasing_form_html,
        "inventory_detail_html":inventory_detail_html,
        "main_material_quota_html":main_material_quota_html,
        "accessory_quota_html":accessory_quota_html,
        "first_send_detail_html":first_send_detail_html,
        "out_purchasing_detail_html":out_purchasing_detail_html,
        "cast_detail_html":cast_detail_html
        })

@dajaxice_register
def pendingOrderSearch(request, order_index):
    """
    JunHU
    summary: ajax function to search the order set by order index
    params: order_index: the index of the work order
    return: table html string
    """
    inventoryTypeForm = InventoryTypeForm()
    orders = WorkOrder.objects.filter(order_index__startswith = order_index)
    context = {"inventoryTypeForm": inventoryTypeForm,
               "orders": orders
              }
    html = render_to_string("purchasing/pending_order/pending_order_table.html", context)
    return html

@dajaxice_register
def getInventoryTable(request, table_id, order_index):
    """
    JunHU
    summary: ajax function to load 5 kinds of inventory table
    params: table_id: the id of table; order_index: the index of work_order
    return: table html string
    """

    #dict of table_id to fact table
    #it should be optimized when database scale expand
    id2table = {
        "1": "main_materiel",
        "2": "auxiliary_materiel",
        "3": "first_feeding",
        "4": "purchased",
        "5": "forging",
    }
    items = Materiel.objects.filter(order__order_index = order_index, inventory_type__id = table_id)
    context = {
        "items": items,
    }
    html = render_to_string("purchasing/inventory_table/%s.html" % id2table[table_id], context)
    
    return html

@dajaxice_register
def addToDetail(request, table_id, order_index):
    """
    JunHU
    summary: ajax function to change all materiels' purchasing status
    params: table_id: the id of table; order_index: the index of work_order
    return: NULL
    """
    items = Materiel.objects.filter(order__order_index = order_index, inventory_type__id = table_id)
    for item in items:
        item.materielpurchasingstatus.add_to_detail = True
        item.materielpurchasingstatus.save()
    return ""

@dajaxice_register
def addToDetailSingle(request, index):
    """
    JunHU
    summary: ajax function to change single materiel's purchasing status
    params: index: database index of materiel
    return: NULL
    """
    item = Materiel.objects.get(id = index)
    item.materielpurchasingstatus.add_to_detail = True
    item.materielpurchasingstatus.save()
    return ""

@dajaxice_register
def SupplierAddorChange(request,mod,supplier_form):
    if mod==-1:
        supplier_form=SupplierForm(deserialize_form(supplier_form))
        supplier_form.save()
    else:
        supplier=Supplier.objects.get(pk=mod)
        supplier_form=SupplierForm(deserialize_form(supplier_form),instance=supplier)
        supplier_form.save()
    table=refresh_supplier_table(request)
    ret={"status":'0',"message":u"供应商添加成功","table":table}
    return simplejson.dumps(ret)

def refresh_supplier_table(request):
    suppliers=Supplier.objects.all()
    context={
        "suppliers":suppliers,
    }
    return render_to_string("purchasing/supplier/supplier_table.html",context)

@dajaxice_register
@transaction.commit_manually
def entryConfirm(request,e_items,pur_entry):
    try:
        if pur_entry["entry_time"] == "" or pur_entry["receipts_code"] == "":
            return simplejson.dumps({"flag":False,"message":u"入库单确认失败，入库时间或单据标号为空"})
        for item in e_items:
            pur_item = PurchasingEntryItems.objects.get(id = item["eid"])
            pur_item.standard = item["standard"]
            pur_item.status = item["status"]
            pur_item.remark = item["remark"]
            pur_item.save()
        pid = pur_entry["pid"]
        entry_time = pur_entry["entry_time"]
        receipts_code = pur_entry["receipts_code"]
        pur_entry = PurchasingEntry.objects.get(id = pid)
        pur_entry.entry_time = entry_time
        pur_entry.receipts_code = receipts_code
        pur_entry.save()
        transaction.commit()
        flag = True
        message = u"入库单确认成功"
    except Exception,e:
        transaction.rollback()
        flag = False
        message = u"入库单确认失败，数据库导入失败"
        print "----error-----"
        print e
        print "--------------"
    data = {
        "flag":flag,
        "message":message,
    }
    return simplejson.dumps(data)

def FileDelete(requset,mod,file_id):
    file=SupplierFile.objects.get(pk=file_id)
    file.delete()
    supplier=Supplier.objects.get(pk=mod)
    supplier_html=render_to_string("purchasing/supplier/supplier_file_table.html",{"supplier":supplier})
    return simplejson.dumps({"supplier_html":supplier_html})

@dajaxice_register
def SupplierDelete(request,supplier_id):
    supplier=Supplier.objects.get(pk=supplier_id)
    supplier.delete()
    return simplejson.dumps({})


@dajaxice_register
def addChangeItem(request,subform,sid,item_id = None):
    subapply = MaterialSubApply.objects.get(id = sid)
    flag = True
    try:
        if item_id == None:
            subform = SubApplyItemForm(deserialize_form(subform))
            if subform.is_valid():
                subitem = subform.save(commit = False)
                subitem.sub_apply = subapply
                subitem.save()
            else:
                flag = False
        else:
            item = MaterialSubApplyItems.objects.get(id = item_id)
            subform = SubApplyItemForm(deserialize_form(subform),instance = item)
            if subform.is_valid():
                subform.save()
            else:
                flag = False
    except Exception,e:
        print e
    sub_item_set = MaterialSubApplyItems.objects.filter(sub_apply = subapply)
    sub_table_html = render_to_string("purchasing/widgets/sub_table.html",{"sub_set":sub_item_set})
    data = {
        "flag":flag,
        "html":sub_table_html,
    }
    return simplejson.dumps(data)

@dajaxice_register
def addSubApply(request):
    subapply = MaterialSubApply( proposer = request.user)
    subapply.save()
    url = "/purchasing/subApply/"+str(subapply.id)
    return simplejson.dumps({"url":url})

@dajaxice_register
def deleteItem(request,item_id,sid):
    item_obj = MaterialSubApplyItems.objects.get(id = item_id)
    subapply = MaterialSubApply.objects.get(id = sid)
    if item_obj.sub_apply.id == subapply.id:
        try:
            item_obj.delete()
            flag = True
        except Exception,e:
            print e
    else:
        flag = False
    return simplejson.dumps({"item_id":item_obj.id,"flag":flag})

