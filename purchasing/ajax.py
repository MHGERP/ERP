# coding: UTF-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from purchasing.models import BidForm,ArrivalInspection,Supplier,SupplierFile,PurchasingEntry,PurchasingEntryItems,MaterialSubApplyItems,MaterialSubApply
from purchasing.models import OrderForm, MaterielExecute, SupplierSelect, BidForm
from purchasing.forms import SupplierForm, BidApplyForm, QualityPriceCardForm, BidCommentForm
from const import *
from const.models import Materiel,OrderFormStatus, BidFormStatus
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib.auth.models import User
from django.db import transaction 
from const.models import WorkOrder, Materiel
from const.forms import InventoryTypeForm
from django.http import HttpResponseRedirect
from purchasing.forms import SupplierForm,ProcessFollowingForm,SubApplyItemForm
from django.db.models import Q
from datetime import datetime


@dajaxice_register
def searchPurchasingFollowing(request,bidid):
    bidform_processing=BidForm.objects.filter(bid_id__contains=bidid)
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
    flag = False
    message = ""
    try:
        bidform = BidForm.objects.get(bid_id = bid)
        user = request.user
        if PurchasingEntry.objects.filter(bidform = bidform).count() == 0:
            purchasingentry = PurchasingEntry(bidform = bidform,purchaser=user,inspector = user , keeper = user) 
            purchasingentry.save()
            flag = True
        else:
            message = u"入库单已经存在，请勿重复提交"
    except Exception, e:
        transaction.rollback()
        print e

    flag = flag and isAllChecked(bid,purchasingentry)
    if flag:
        transaction.commit()
        message = u"入库单生成成功"
    else:
        transaction.rollback()
        if message =="":
            message = u"入库单生成失败，有未确认的项，请仔细检查"
    data = {
        'flag':flag,
        'message':message,
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
def chooseInventorytype(request,pid,key):
    idtable = {
        "1": "main_materiel",
        "2": "auxiliary_materiel",
        "3": "first_feeding",
        "4": "purchased",
        "5": "forging",
    }
    items = Materiel.objects.filter(inventory_type__id=pid, materielpurchasingstatus__add_to_detail = True)
    if key:
        items = items.filter(name=key)
    context={
        "inventory_detail_list":items,
    }
    inventory_detail_html = render_to_string("purchasing/inventory_detail_table/%s.html" % idtable[pid], context)
    new_order_form_html = render_to_string("widgets/new_order_form.html",context)
    new_purchasing_form_html = render_to_string("widgets/new_purchasing_form.html",context)
    return simplejson.dumps({
        "new_order_form_html":new_order_form_html,
        "new_purchasing_form_html":new_purchasing_form_html,
        "inventory_detail_html":inventory_detail_html
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
def getOrderFormList(request, statu, key):
    """
    JunHU
    summary: ajax function to get the order form list by statu & keyword
    params: statu: the statu of request; key: keyword string(empty or NULL should be ignore)
    return: table html string
    """
    try:
        statu = int(statu) # unicode to integer
    
        items = OrderForm.objects.filter(order_status__status = statu)
        if key:
            items = items.filter(order_id = key)
    except Exception, e:
        print e
    context = {"items": items, }
    html = render_to_string("purchasing/orderform/orderform_list.html", context)
    return html

@dajaxice_register
def SupplierAddorChange(request,mod,supplier_form):
    message=u"供应商添加成功！"
    if mod==-1:
        supplier_form=SupplierForm(deserialize_form(supplier_form))
        if supplier_form.is_valid():
            supplier_form.save()
        else:
            message=u"添加失败,供应商编号和供应商名称不能为空！"
    else:
        supplier=Supplier.objects.get(pk=mod)
        supplier_form=SupplierForm(deserialize_form(supplier_form),instance=supplier)
        if supplier_form.is_valid():
            supplier_form.save()
        else:
            message=u"修改失败,供应商编号和供应商名称不能为空！"
    table=refresh_supplier_table(request)
    ret={"status":'0',"message":message,"table":table}
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
def MaterielExecuteQuery(request,number):
    materielexecute = MaterielExecute.objects.filter(document_number=number)
    materielexecute_html = render_to_string("purchasing/materielexecute/materielexecute_table.html", {"materielexecute_set":materielexecute})
    return simplejson.dumps({"materielexecute_html":materielexecute_html})
def SelectSupplierOperation(request,selected,bid):
    bidform=BidForm.objects.get(pk=bid)
    for item in selected:
        item=int(item)
        supplier=Supplier.objects.get(pk=item)
        select_supplier=SupplierSelect.objects.filter(bidform=bidform,supplier=supplier)
        if select_supplier.count()==0:
            supplier_select_item=SupplierSelect(bidform=bidform,supplier=supplier)
            supplier_select_item.save()
    return simplejson.dumps({"status":u"选择成功"})

@dajaxice_register
def SelectSupplierReset(request,bid):
    select_items=SupplierSelect.objects.filter(bidform__id=bid)
    select_items.delete()
    return simplejson.dumps({"status":u"重置成功"})


@dajaxice_register
def searchSupplier(request,sid,bid):
    suppliers=Supplier.objects.filter(Q(supplier_id__contains=sid)|Q(supplier_name__contains=sid))
    bidform=BidForm.objects.get(pk=bid)
    for item in suppliers:
        if SupplierSelect.objects.filter(supplier=item,bidform=bidform).count()>0:
            item.selected=1
        else:
            item.selected=0
    context={
        "suppliers":suppliers,
    }
    supplier_select_html=render_to_string("purchasing/supplier/supplier_select_table.html",context)
    data={
        'html':supplier_select_html
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

@dajaxice_register
def deleteDetail(request,uid):
    item = Materiel.objects.get(id = uid)
    item.materielpurchasingstatus.add_to_detail = False
    item.materielpurchasingstatus.save()
    param = {"uid":uid}
    return simplejson.dumps(param)

@dajaxice_register
def saveComment(request, form, bid_id):
    bidCommentForm = BidCommentForm(deserialize_form(form))
    if bidCommentForm.is_valid():
        bid = BidForm.objects.get(bid_id = bid_id)
        if bid != None:
            bid_comment = BidComment()
            bid_comment.user = request.user
            bid_comment.comment = bidCommentForm.cleaned_data["judgeresult"]
            bid_comment.bid = bid
            bid_comment.save()
            ret = {'status': '0', 'message': u"添加成功"}
        else:
            ret = {'status': '1', 'message': u"该成员不存在，请刷新页面"}
    else:
        ret = {'status': '1', 'message': u"该成员不存在，请刷新页面"}
    return simplejson.dumps(ret)
def AddProcessFollowing(request,bid,process_form):
    process_form=ProcessFollowingForm(deserialize_form(process_form))
    if process_form.is_valid():
        process_form.save()
    else:
        print process_form.errors
    return simplejson.dumps({})
def newOrderSave(request,num,cDate,eDate):
    cDate_datetime = datetime.datetime.strptime(cDate,"%Y-%m-%d")
    eDate_datetime = datetime.datetime.strptime(eDate,"%Y-%m-%d")
    order_status = OrderFormStatus.objects.get(status=0)
    order_obj = OrderForm(
        order_id = str(num),
        create_time = cDate_datetime,
        establishment_time = eDate_datetime,
        order_status = order_status
    )
    order_obj.save()

@dajaxice_register
def newOrderFinish(request,num,cDate,eDate):
    cDate_datetime = datetime.datetime.strptime(cDate,"%Y-%m-%d")
    eDate_datetime = datetime.datetime.strptime(eDate,"%Y-%m-%d")
    order_status = OrderFormStatus.objects.get(status=1)
    order_obj = OrderForm(
        order_id = str(num),
        create_time = cDate_datetime,
        establishment_time = eDate_datetime,
        order_status = order_status
    )
    order_obj.save()

@dajaxice_register
def newOrderDelete(request,num):
    order = OrderForm.objects.get(order_id = num)
    order.delete()

@dajaxice_register
def getOrderFormItems(request, index):
    """
    JunHU
    """
    items = Materiel.objects.filter(materielformconnection__order_form__order_id = index)
    context = {
        "items": items,
    }
    html = render_to_string("purchasing/orderform/orderform_item_list.html", context)
    return html

@dajaxice_register
def newBidCreate(request):
    cDate_datetime = datetime.now()
    print datetime.now()
    bid_status = BidFormStatus.objects.get(part_status = BIDFORM_PART_STATUS_CREATE)
    bid_form = BidForm(
        bid_id = "2015000%d" % (BidForm.objects.count()),
        create_time = cDate_datetime,
        bid_status = bid_status,
    )
    bid_form.save()
    html = render_to_string("purchasing/orderform/orderform_item_list.html", {})
    context = {
        "bid_id": bid_form.bid_id,
        "html": html,
    }
    return simplejson.dumps(context)

@dajaxice_register
def getBidForm(request, bid_id):
    """
    JunHU
    """
    bid_form = BidForm.objects.get(id = bid_id)
    items = Materiel.objects.filter(materielformconnection__bid_form = bid_form)
    html = render_to_string("purchasing/orderform/orderform_item_list.html", {"items": items})
    context = {
            "bid_id": bid_form.bid_id,
            "html": html,
        }

    return simplejson.dumps(context)

