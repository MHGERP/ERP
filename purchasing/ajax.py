# coding: UTF-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from purchasing.models import *
from purchasing.forms import SupplierForm, BidApplyForm, QualityPriceCardForm, BidCommentForm,OrderFormForm, ContractDetailForm, MeterielExcecuteForm
from const import *
from purchasing import *
from const.models import OrderFormStatus, BidFormStatus
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib.auth.models import User
from django.db import transaction
from const.models import WorkOrder,Material, InventoryType
from const.forms import InventoryTypeForm
from django.http import HttpResponseRedirect
from purchasing.forms import *
from django.db.models import Q
from purchasing.utility import goNextStatus,goStopStatus,buildArrivalItems,BidNextStatus
from storage.models import *
from storage.forms import EntryTypeForm
from storage.utils import AutoGenEntry
from purchasing.models import MaterielCopy as Materiel
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
    val = getattr(cargo_obj,arrivalfield)
    if not cargo_obj.check_pass:
        if not val:
            setattr(cargo_obj,arrivalfield,not val)
            cargo_obj.save()
            message = u"状态修改成功"
            isOk = True
    else:
        message = u"状态修改失败"
        isOk = False
    isForbiden = cargo_obj.material_confirm and cargo_obj.soft_confirm and cargo_obj.inspect_confirm
    data = {
        "message":message,
        'isOk':isOk,
        "isForbiden":isForbiden,
        "aid":aid,
    }
    return simplejson.dumps(data)

#@dajaxice_register
#@transaction.commit_manually
#def genEntry(request,bid,selected):
#    print selected
#    flag = False
#    message = ""
#    try:
#        bidform = BidForm.objects.get(bid_id = bid)
#        user = request.user
#        if PurchasingEntry.objects.filter(bidform = bidform).count() == 0:
#            purchasingentry = PurchasingEntry(bidform = bidform,purchaser=user,inspector = user , keeper = user)
#            purchasingentry.save()
#            goNextStatus(bidform,request.user)
#            flag = True
#        else:
#            message = u"入库单已经存在，请勿重复提交"
#    except Exception, e:
#        transaction.rollback()
#        print e
#
#    flag = flag and isAllChecked(bid,purchasingentry)
#    if flag:
#        transaction.commit()
#        message = u"入库单生成成功"
#    else:
#        transaction.rollback()
#        if message =="":
#            message = u"入库单生成失败，有未确认的项，请仔细检查"
#
#    data = {
#        'flag':flag,
#        'message':message,
#    }
#    return simplejson.dumps(data)

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
    """
    Lei
    """
    idtable = {
        MAIN_MATERIEL: "main_materiel",
        AUXILIARY_MATERIEL: "auxiliary_materiel",
        FIRST_FEEDING: "first_feeding",
        OUT_PURCHASED: "purchased",
        COOPERANT: "forging",
        WELD_MATERIAL: "weld_material",
    }
    items = Materiel.objects.filter(inventory_type__name=pid, materielpurchasingstatus__add_to_detail = True,relate_material=None)
    print pid
    print ("item的size:" + str(len(items)))
    if key:
        items = items.filter(name=key)
    for item in items:
        if MaterielFormConnection.objects.filter(materiel = item).count() == 0:
            MaterielFormConnection(materiel = item, count = item.count).save()
        inventory_type=item.inventory_type.all()[0]
        if inventory_type.name ==  MAIN_MATERIEL or  inventory_type.name == AUXILIARY_MATERIEL:
            if item.materielexecutedetail_set.count()>0 or item.materielformconnection.order_form:
                item.can_choose=False
                item.status= u"已加入订购单" if (item.materielformconnection.order_form) else u"已加入材料执行"
            else :
                item.can_choose=True
                item.status=u"未处理"
        else:
            item.can_choose, item.status = (False, u"已加入订购单") if (item.materielformconnection.order_form != None) else (True, u"未加入订购单")

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
def getRelatedModel(request, index):
    idtable = {
        MAIN_MATERIEL: "main_materiel",
        AUXILIARY_MATERIEL: "auxiliary_materiel",
        FIRST_FEEDING: "first_feeding",
        OUT_PURCHASED: "purchased",
        COOPERANT: "forging",
        WELD_MATERIAL: "weld_material",
    }
    data = []
    print "这是一个测试: "
    print index
    if index == MAIN_MATERIEL:
        data = SteelMaterialStoreList.objects.all()
    elif index == AUXILIARY_MATERIEL:
        data = SteelMaterialStoreList.objects.all()
    elif index == FIRST_FEEDING:
        print index
    elif index == OUT_PURCHASED:
        data = OutsideStorageList.objects.all()
    elif index == COOPERANT:
        print index
    elif index == WELD_MATERIAL:
        data = WeldStoreList.objects.all()
    context={
        "data" : data
    }
    return render_to_string("purchasing/related_model/%s.html" % idtable[index], context)

@dajaxice_register
def getRelatedTable(request, index, f1, f2, f3):
    idtable = {
        MAIN_MATERIEL: "main_materiel",
        AUXILIARY_MATERIEL: "auxiliary_materiel",
        FIRST_FEEDING: "first_feeding",
        OUT_PURCHASED: "purchased",
        COOPERANT: "forging",
        WELD_MATERIAL: "weld_material",
    }
    data = []
    if index == MAIN_MATERIEL or index == AUXILIARY_MATERIEL:
        data = SteelMaterialStoreList.objects.filter(name = f1, specifications = f2, material = f3)
    elif index == OUT_PURCHASED:
        data = OutsideStorageList.objects.filter(texture = f2)
        print data
    elif index == WELD_MATERIAL:
        data = WeldStoreList.objects.filter(entry_item__specifimaterial_mark = f2 , entry_item__specifications = f3)
    context = {
        "data" : data,
    }
    return render_to_string("purchasing/related_table/%s.html" % idtable[index], context)

@dajaxice_register
def addToForeign(request, index):
    item = Materiel.objects.get(id = index)
    item.inventory_type.clear()
    item.inventory_type.add(InventoryType.objects.get(name = OUT_PURCHASED))
    return ""


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
        MAIN_MATERIEL: "main_materiel",
        AUXILIARY_MATERIEL: "auxiliary_materiel",
        FIRST_FEEDING: "first_feeding",
        OUT_PURCHASED: "purchased",
        COOPERANT: "forging",
        WELD_MATERIAL: "weld_material",

    }
    items = Materiel.objects.filter(order__order_index = order_index, inventory_type__name = table_id)
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
        try:
            item.materielpurchasingstatus.add_to_detail = True
            item.materielpurchasingstatus.save()
        except:
            status = MaterielPurchasingStatus(materiel = item, add_to_detail = True)
            status.save()
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
    try:
        item.materielpurchasingstatus.add_to_detail = True
        item.materielpurchasingstatus.save()
    except:
        status = MaterielPurchasingStatus(materiel = item, add_to_detail = True)
        status.save()
    return ""

@dajaxice_register
def deleteOrderForm(request, index):
    """
    JunHU
    """
    order_form = OrderForm.objects.get(order_id = index)
    order_form.delete()

@dajaxice_register
def finishOrderForm(request, index):
    """
    JunHU
    """
    order_form = OrderForm.objects.get(order_id = index)
    order_form.order_status = OrderFormStatus.objects.get(status = ORDERFORN_STATUS_FINISH)
    order_form.save()

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
    context = {
        "items": items,
        "ORDERFORN_STATUS_BEGIN": ORDERFORN_STATUS_BEGIN,
        "ORDERFORN_STATUS_ESTABLISHMENT": ORDERFORN_STATUS_ESTABLISHMENT,
    }
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

        pid = pur_entry["pid"]
        pur_obj = PurchasingEntry.objects.get(id = pid)
        bidform = pur_obj.bidform
        flag = True
        if bidform.bid_status.part_status != BIDFORM_PART_STATUS_STORE:
            flag = False
            message=u"入库单已经确认过，请勿重复确认"
        if pur_entry["entry_time"] == "":
            flag=False
            message=u"入库单确认失败，入库时间为空"
        for item in e_items:
            pur_item = PurchasingEntryItems.objects.get(id = item["eid"])
            pur_item.standard = item["standard"]
            pur_item.status = item["status"]
            pur_item.remark = item["remark"]
            pur_item.save()
        pur_obj.entry_time = pur_entry["entry_time"]
        pur_obj.save()
        if flag:
            goNextStatus(bidform,request.user)
            message = u"入库单确认成功"
    except Exception,e:
        flag = False
        message = u"入库单确认失败，数据库导入失败"
        print "----error-----"
        print e
        print "--------------"
    finally:
        if flag:
            transaction.commit()
        else:
            transaction.rollback()
        data ={
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
    is_pass = subapply.is_submit
    flag = True
    try:
        if item_id == None:
            subform = SubApplyItemForm(deserialize_form(subform))
            print subform
            if subform.is_valid():
                subitem = subform.save(commit = False)
                subitem.sub_apply = subapply
                if not is_pass:
                    subitem.save()
                    message = u"添加成功"
            else:
                flag = False
        else:
            item = MaterialSubApplyItems.objects.get(id = item_id)
            print subform
            subform = SubApplyItemForm(deserialize_form(subform),instance = item)
            if subform.is_valid():
                if not is_pass:
                    subform.save()
                    message = u"修改成功"
            else:
                flag = False
    except Exception,e:
        print e
    if not flag:
        message = u"添加失败，请确认所有内容填写完整"
    if is_pass:
        message = u"添加失败，申请表已经提交不能再修改"
    sub_item_set = MaterialSubApplyItems.objects.filter(sub_apply = subapply)
    sub_table_html = render_to_string("purchasing/widgets/sub_table.html",{"sub_set":sub_item_set})
    data = {
        "flag":flag,
        "html":sub_table_html,
        "message":message,
    }
    return simplejson.dumps(data)
@dajaxice_register
def materielExecuteQuery(request,number):
    """
    mxl
    summary : query a materielexecute by document_number
    params : number : the document_number to query database
    """
    materielexecute = MaterielExecute.objects.filter(document_number=number)
    materielexecute_html = render_to_string("purchasing/materielexecute/table/materielexecute_table.html", {"materielexecute_set":materielexecute})
    return simplejson.dumps({"materielexecute_html":materielexecute_html})

@dajaxice_register
def materielchoiceChange(request, materielChoice):
    """
    mxl
    summary : when the select widget change between main and support, the table style and data woule be changed
    params : materielChoice : the selected materiel_choice
    """
    print materielChoice
    if materielChoice == MAIN_MATERIEL:
        # materielexecute_detail_set = MainMaterielExecuteDetail.objects.all()
        #detailForm = MainMaterielExecuteDetailForm()
        materielexecute_detail_html = "purchasing/materielexecute/table/main_materielexecute_detail_table.html"
        #formname = "MainMaterielExecuteDetailForm"
        #add_form = render_to_string("purchasing/materielexecute/widget/add_main_detail_form.html", {"MainMaterielExecuteDetailForm":detailForm})
        current_materiel_choice = MATERIEL_CHOICE[0][1]
        materiels=MaterielExecuteDetail.objects.filter(materiel__inventory_type__id=1,materiel_execute__isnull=True)
        select_materielexecute_html=render_to_string("purchasing/materielexecute/table/select_main_materielexecute.html",{"materiels":materiels})
    else:
        # materielexecute_detail_set = SupportMaterielExecuteDetail.objects.all()
        #detailForm = SupportMaterielExecuteDetailForm()
        materielexecute_detail_html = "purchasing/materielexecute/table/support_materielexecute_detail_table.html"
        #formname = "SupportMaterielExecuteDetailForm"
        #add_form = render_to_string("purchasing/materielexecute/widget/add_support_detail_form.html", {"SupportMaterielExecuteDetailForm":detailForm})
        current_materiel_choice = MATERIEL_CHOICE[1][1]
        materiels=MaterielExecuteDetail.objects.filter(materiel__inventory_type__id=2,materiel_execute__isnull=True)
        select_materielexecute_html=render_to_string("purchasing/materielexecute/table/select_support_materielexecute.html",{"materiels":materiels})
    # choice_form = MaterielChoiceForm()
    context = {
        "choice" : SUPPORT_MATERIEL,
        "MAIN_MATERIEL" : MAIN_MATERIEL
        # "materielChoice_form" : choice_form,
        #formname : detailForm
    }
    rendered_materielexecute_detail_html = render_to_string(materielexecute_detail_html, context)
    return_context={
        'materielexecute_detail_html' : rendered_materielexecute_detail_html,
        #'add_form' : add_form,
        'current_materiel_choice' : current_materiel_choice,
        'select_materielexecute_html':select_materielexecute_html
    }
    return simplejson.dumps(return_context)

@dajaxice_register
def saveMaterielExecute(request, form):
    materielExecuteForm = MaterielExecuteForm(deserialize_form(form))
    if materielExecuteForm.is_valid():
        materielexecute = MaterielExecute();
        # materielExecuteForm.save()
        materielexecute.document_number = materielExecuteForm.cleaned_data["document_number"]
        materielexecute.materiel_choice = materielExecuteForm.cleaned_data["materiel_choice"]
        materielexecute.document_lister = request.user
        materielexecute.date = datetime.today()
        materielexecute.is_save = False
        materielexecute.save()
        ret = {'status' : '1', 'message' : u'材料执行保存成功！', 'materielChoice' : materielexecute.materiel_choice, 'materielExecuteId' : materielexecute.id}
    else:
        ret = {'status' : '0', 'message' : u'材料执行保存失败！'}
    return simplejson.dumps(ret)

@dajaxice_register
def saveMaterielExecuteDetail(request, selected, eid):
    materielexecute=MaterielExecute.objects.get(document_number=eid)
    for item in selected:
        print item
        materielexecutedetail=MaterielExecuteDetail.objects.get(pk=item)
        materielexecutedetail.materiel_execute=materielexecute
        materielexecutedetail.save()

    return simplejson.dumps({"status":u"添加成功!"})
@dajaxice_register
def materielExecuteCommit(request,  materielExecuteId):
    try:
        print materielExecuteId
        materielexecute=MaterielExecute.objects.get(document_number=materielExecuteId)
        materielexecute.is_save=True
        materielexecute.date=datetime.today()
        materielexecute.save()
        ret = {'status' :0,'message':u'材料执行表提交成功！',}
    except Exception, e:
        print e
        ret = {'status' :1,'message': u'提交失败！'}
    return simplejson.dumps(ret)

@dajaxice_register
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
    """
    Lei
    """
    item = Materiel.objects.get(id = uid)
    item.materielpurchasingstatus.add_to_detail = False
    item.materielpurchasingstatus.save()

    item.materielformconnection.delete()  # by JunHU

    param = {"uid":uid}
    return simplejson.dumps(param)

@dajaxice_register
def contractAmount(request, tid, bid,  form):
    if tid == CONTRACT_ADD_AMOUNT:
        table = render_to_string("purchasing/widgets/contract_detail_form.html", {"ContractDetailForm": ContractDetailForm(),
                                                                                  "CONTRACT_ADD_DETAIL": CONTRACT_ADD_DETAIL,
                                                                                  "bid":bid})
        ret = {'status': '1', 'table': table}
    elif tid == CONTRACT_DETAIL:
        bidform = BidForm.objects.get(bid_id = bid)
        contractDetails = ContractDetail.objects.filter(bidform = bidform)
        table = render_to_string("purchasing/widgets/contract_detail.html", {"contractDetails": contractDetails})
        ret = {'status': '1', 'table': table}
    elif tid == CONTRACT_ADD_DETAIL:
        contractDetailForm = ContractDetailForm(deserialize_form(form))
        bidform = BidForm.objects.get(bid_id = bid)
        if contractDetailForm.is_valid():
            amount = int(contractDetailForm.cleaned_data["amount"])
            if amount <= bidform.payable_amount():
                contractDetail = contractDetailForm.save(commit = False)
                contractDetail.user = request.user
                contractDetail.bidform = bidform
                contractDetail.save()
                return simplejson.dumps({'status': '0', 'message': u"合同金额添加成功"})
            else:
                return simplejson.dumps({'status': '2', 'message': u"合同金额添加应小于应付金额"})
        if message == "":
            message = u"合同金额添加失败"
        ret = {'status': '2', 'message': message}
        print ret
    else:
        pass
    return simplejson.dumps(ret)

@dajaxice_register
def saveComment(request, form, bid_id):
    bidCommentForm = BidCommentForm(deserialize_form(form))
    if bidCommentForm.is_valid():
        bid = BidForm.objects.get(id = bid_id)
        judge = bidCommentForm.cleaned_data["judgeresult"]
        if judge in ("1", "0") and bid != None:
            bid_comment = BidComment()
            bid_comment.user = request.user
            bid_comment.comment = bidCommentForm.cleaned_data["reason"]
            bid_comment.bid = bid
            bid_comment.result = int(judge)
            bid_comment.status = BIDFORM_STATUS_INVITE_BID
            bid_comment.save()
            print judge
            if judge == "0":
                print "ok"
                goNextStatus(bid, request.user)
            else:
                pass
            ret = {'status': '1', 'message': u"评审意见提交成功"}
        else:
            ret = {'status': '0', 'message': u"评审意见提交不成功"}
    else:
        ret = {'status': '0', 'message': u"评审意见提交不成功"}
    return simplejson.dumps(ret)

@dajaxice_register
def saveBidApply(request, form, bid_apply_id):
    bid_apply=bidApply.objects.get(pk=bid_apply_id)
    bidApplyForm = BidApplyForm(deserialize_form(form), instance=bid_apply)
    if bidApplyForm.is_valid():
        bidApplyForm.save()
        ret = {'status': '2', 'message': u"申请书保存成功"}
    else:
        ret = {'status': '0', 'field':bidApplyForm.data.keys(), 'error_id':bidApplyForm.errors.keys(), 'message': u"申请书保存不成功"}
    return simplejson.dumps(ret)

@dajaxice_register
def resetBidApply(request, bid_id):
    try:
        bidform = BidForm.objects.get(id = bid_id)
        bidapply = bidApply.objects.get(bid = bidform)
        bidapply.delete()
        ret = {'status': '1', 'message': u"申请书重置成功"}
    except:
        ret = {'status': '2', 'message': u"申请书信息不存在"}
    return simplejson.dumps(ret)

@dajaxice_register
def submitBidApply(request, bid_apply_id):
    bid_apply = bidApply.objects.get(id = bid_apply_id)
    BidNextStatus(bid_apply)
    return simplejson.dumps({})


def AddProcessFollowing(request,bid,process_form):
    process_form=ProcessFollowingForm(deserialize_form(process_form))
    if process_form.is_valid():
        process_form.save()
    else:
        print process_form.errors
    return simplejson.dumps({})

def getMaxId(table):
    try:
        return max(int(item.id) for item in table.objects.all())
    except:
        return -1

@dajaxice_register
def getOrderFormItems(request, index, can_choose = False):
    """
    JunHU
    """
    items = Materiel.objects.filter(materielformconnection__order_form__order_id = index)
    order_form=OrderForm.objects.get(order_id=index)
    for item in items:
        item.can_choose, item.order_status = (False, u"已加入标单") if (item.materielformconnection.bid_form != None) else (True, u"未加入标单")

    context = {
        "items": items,
        "order_form":order_form,
        "can_choose": can_choose,
    }
    if order_form.order_mod==1:
        html = render_to_string("purchasing/orderform/orderform_item_list.html", context)
    else:
        html =render_to_string("purchasing/orderform/orderform_raw_list.html",context)
    return html

@dajaxice_register
def SelectSubmit(request,bid):
    bidform=BidForm.objects.get(pk=bid)
    if bidform.bid_status.part_status != BIDFORM_PART_STATUS_SELECT_SUPPLLER_APPROVED:
        status=2
    elif SupplierSelect.objects.filter(bidform=bidform).count() > 0:
        goNextStatus(bidform,request.user)
        status=0
    else:
        status=1
    return simplejson.dumps({"status":status})


@dajaxice_register
def ProcessFollowingSubmit(request,bid):
    bidform=BidForm.objects.get(pk=bid)
    if bidform.bid_status.part_status == BIDFORM_PART_STATUS_PROCESS_FOLLOW:
        goNextStatus(bidform,request.user)
        buildArrivalItems(bidform)
        status=0
    else :
        status=1
    return simplejson.dumps({"status":status})

@dajaxice_register
def getOngoingBidList(request):
    """
    JunHU
    """
    bid_form_list = BidForm.objects.filter(Q(bid_status__part_status = BIDFORM_PART_STATUS_CREATE) | Q(bid_status__part_status = BIDFORM_PART_STATUS_ESTABLISHMENT))
    html = ''.join("<option value='%s'>%s</option>" % (bid.id, bid) for bid in bid_form_list)
    return html

@dajaxice_register
def getOngoingOrderList(request,order_type):
    """
    Lei
    """
    if int(order_type) >2 :
        order_mod=1
    else:
        order_mod=0
    order_form_list = OrderForm.objects.filter(Q(order_status__status = 0)&Q(order_mod=order_mod))
    html = ''.join("<option value='%s'>%s</option>" % (order.id, order) for order in order_form_list)
    return html

@dajaxice_register
def newBidCreate(request):
    """
    JunHU
    """
    cDate_datetime = datetime.now()
    bid_status = BidFormStatus.objects.get(part_status = BIDFORM_PART_STATUS_CREATE)
    bid_form = BidForm(
        bid_id = "2015%05d" % (getMaxId(BidForm) + 1),
        create_time = cDate_datetime,
        bid_status = bid_status,
    )
    bid_form.save()
    html = render_to_string("purchasing/orderform/orderform_item_list.html", {})
    context = {
        "bid_id": bid_form.bid_id,
        "id": bid_form.id,
        "html": html,
    }
    return simplejson.dumps(context)

@dajaxice_register
def newOrderCreate(request,select_type):
    """
    Lei
    """
    cDate_datetime = datetime.now()
    if int(select_type) > 2:
        order_type=1
    else:
        order_type=0
    order_status = OrderFormStatus.objects.get(status = 0)
    order_form = OrderForm(
        order_id = "2015%05d" % (getMaxId(OrderForm) + 1),
        create_time = cDate_datetime,
        order_status = order_status,
        order_mod=order_type
    )
    order_form.save()
    html = render_to_string("purchasing/orderform/orderform_item_list.html", {})
    context = {
        "order_id":order_form.order_id,
        "id": order_form.id,
        "html":html,
    }
    return simplejson.dumps(context)

@dajaxice_register
def newBidSave(request, id, pendingArray):
    """
    JunHU
    """
    cDate_datetime = datetime.now()
    bid_form = BidForm.objects.get(id = id)
    for id in pendingArray:
        materiel = Materiel.objects.get(id = id)
        try:
            conn = MaterielFormConnection.objects.get(materiel = materiel)
        except:
            conn = MaterielFormConnection(materiel = materiel)
        conn.bid_form = bid_form
        conn.save()
    bid_form.establishment_time = cDate_datetime
    bid_form.save()

@dajaxice_register
def newOrderSave(request, id, pendingArray):
    """
    Lei
    """
    #addToExecute(pendingArray)
    cDate_datetime = datetime.now()
    order_form = OrderForm.objects.get(id = id)
    for id in pendingArray:
        materiel = Materiel.objects.get(id = id)
        #if materiel.inventory_type.id <= 2:
        #    addToExecute(materiel)
        try:
            conn = MaterielFormConnection.objects.get(materiel = materiel)
        except:
            conn = MaterielFormConnection(materiel = materiel)
        print type(materiel.count)
        conn.order_form = order_form
        conn.count=int(materiel.count)
        conn.save()
    order_form.establishment_time = cDate_datetime
    order_form.save()

@dajaxice_register
def newBidFinish(request, id):
    """
    JunHu
    """
    cDate_datetime = datetime.now()
    bid_form = BidForm.objects.get(id = id)
    bid_form.bid_status = BidFormStatus.objects.get(part_status = BIDFORM_PART_STATUS_APPROVED) # change the part-status into approved
    bid_form.establishment_time = cDate_datetime
    bid_form.save()

@dajaxice_register
def newOrderFinish(request,id):
    """
    Lei
    """
    cDate_datetime = datetime.now()
    order_form = OrderForm.objects.get(id = id)
    order_form.order_status = OrderFormStatus.objects.get(status = 1)
    order_form.establishment_time = cDate_datetime
    order_form.save()

@dajaxice_register
def newBidDelete(request, id):
    """
    JunHU
    """
    bid_form = BidForm.objects.get(id = id)
    bid_form.delete();

@dajaxice_register
def newOrderDelete(request,id):
    """
    Lei
    """
    order_form = OrderForm.objects.get(id = id)
    order_form.delete()

@dajaxice_register
def getBidForm(request, bid_id, pendingArray):
    """
    JunHU
    """
    bid_form = BidForm.objects.get(id = bid_id)
    items = Materiel.objects.filter(materielformconnection__bid_form = bid_form)
    for item in items:
        item.order_status = u"已加入"

    items_pending = [Materiel.objects.get(id = id) for id in pendingArray]
    for item in items_pending:
        item.order_status = u"待加入"

    html = render_to_string("purchasing/orderform/orderform_item_list.html", {"items": items, "can_choose": False, "items_pending": items_pending, })
    context = {
            "bid_id": bid_form.bid_id,
            "id": bid_form.id,
            "html": html,
        }

    return simplejson.dumps(context)

@dajaxice_register
def getOrderForm(request, order_id, pendingArray):
    """
    Lei
    """
    order_form = OrderForm.objects.get(id = order_id)
    items = Materiel.objects.filter(materielformconnection__order_form = order_form)
    for item in items:
        item.order_status = u"已加入"

    items_pending = [Materiel.objects.get(id = id) for id in pendingArray]
    for item in items_pending:
        item.order_status = u"待加入"

    if order_form.order_mod == 1:
        html = render_to_string("purchasing/orderform/orderform_item_list.html", {"items": items, "can_choose": False, "items_pending": items_pending, })
    else:
        html=render_to_string("purchasing/orderform/orderform_raw_list.html",{"items":items,"can_choose":False,"items_pending":items_pending})
    context = {
            "order_id": order_form.order_id,
            "id": order_form.id,
            "html": html,
        }

    return simplejson.dumps(context)

@dajaxice_register
def ProcessFollowingReset(request,bid):
    bidform=BidForm.objects.get(pk=bid)
    process_follows=ProcessFollowingInfo.objects.filter(bidform=bidform)
    process_follows.delete()
    return simplejson.dumps({})

@dajaxice_register
def BidformApprove(request,bid,value,comment):
    bidform=BidForm.objects.get(id=bid)
    if bidform.bid_status.part_status == BIDFORM_PART_STATUS_APPROVED:
        bidcomment=BidComment()
        bidcomment.user=request.user
        bidcomment.comment=comment
        bidcomment.bid=bidform
        bidcomment.submit_date=datetime.today()
        bidcomment.result=value
        bidcomment.status=BIDFORM_STATUS_CREATE
        bidcomment.save()
        if int(value) == APPROVED_PASS:
            status=0
            goNextStatus(bidform,request.user)
        else:
            status=1
            goStopStatus(bidform,request.user)

    else:
        status=-1
    return simplejson.dumps({"status":status})

@dajaxice_register
def GetOrderInfoForm(request,uid):
    """
    Lei
    """
    order = Materiel.objects.get(id=uid)
    count = order.materielformconnection.count
    purchasing=order.materielformconnection.purchasing
    orderForm = OrderFormForm(instance=order)
    form_html = render_to_string("purchasing/orderform/order_form.html",{'order_form':orderForm,'count':count,'purchasing':purchasing})
    return simplejson.dumps({'form':form_html})

@dajaxice_register
def OrderInfo(request,uid,form,count,purchasing):
    """
    Lei
    """
    materiel = Materiel.objects.get(id=uid)
    materielform = OrderFormForm(deserialize_form(form),instance=materiel)
    #order_obj = orderForm.save(commit = False)
    materiel.save()
    matconnection = materiel.materielformconnection
    matconnection.count = count
    matconnection.purchasing=purchasing
    matconnection.save()
    #material = Material.objects.get(name = name)
    #order_obj.material = material
    #order_obj.save()


def addToExecute(materiel):
    materiel_execute_detail=MaterielExecuteDetail(materiel=materiel)
    materiel_execute_detail.save()



@dajaxice_register
def AddToMaterialExecute(request,selected):
    materiel_set=[Materiel.objects.get(pk=item) for item in selected]
    for item in materiel_set:
        if item.materielexecutedetail_set.count()>0:
            return simplejson.dumps({'message':'所选物料已经添加至材料执行'})
    for item in materiel_set:
        materiel=Materiel.objects.get(pk=item)
        addToExecute(materiel)
    return simplejson.dumps({'message':''})

@dajaxice_register
def GetMeterielExecuteForm(request,uid):
    """
    Lei
    """
    materielexecute = MaterielExecuteDetail.objects.get(id=uid)
    materielexecuteForm = MeterielExcecuteForm(instance=materielexecute)
    form_html = render_to_string("widgets/materielexecute_form.html",{'materielexecute_form':materielexecuteForm})
    return simplejson.dumps({'form':form_html})

@dajaxice_register
def materielExecuteInfo(request,form,uid):
    """
    Lei
    """
    materielexecute = MaterielExecuteDetail.objects.get(id=uid)
    materielexecuteForm = MeterielExcecuteForm(deserialize_form(form),instance=materielexecute)
    materielexecute_obj = materielexecuteForm.save()
    materielexecute_obj.save()
    print materielexecute_obj

@dajaxice_register
def OrderFormFinish(request,index,number,revised_id):
    order_form=OrderForm.objects.get(order_id=index)
    order_form.order_status=OrderFormStatus.objects.get(status=1)
    order_form.establishment_time=datetime.now()
    order_form.establishment_user=request.user
    order_form.number=number
    order_form.revised_id=revised_id
    items=MaterielCopy.objects.filter(materielformconnection__order_form__order_id=index)
    work_order=[]
    for item in items:
        if item.work_order:
            item_work=item.work_order.split(',')
            work_order=work_order+item_work
    work_order=set(work_order)
    order_form.work_order=','.join(work_order)
    order_form.save()
    #html=render_to_string("purchasing/orderform/order_form_raw.html",{'order_form':order_form,'items':items})
    return simplejson.dumps({})

@dajaxice_register
def OrderFormAudit(request,index):
    order_form=OrderForm.objects.get(order_id=index)
    order_form.order_status=OrderFormStatus.objects.get(status=2)
    order_form.chief=request.user
    order_form.audit_time=datetime.now()
    order_form.save()
    return simplejson.dumps({})

@dajaxice_register
def OrderFormApprove(request,index):
    order_form=OrderForm.objects.get(order_id=index)
    order_form.order_status=OrderFormStatus.objects.get(status=3)
    order_form.approve_user=request.user
    order_form.approved_time=datetime.now()
    order_form.save()
    return simplejson.dumps({})

@dajaxice_register
def saveTechRequire(request,order_id,content):
    order_form=OrderForm.objects.get(order_id=order_id)
    order_form.tech_requirement=content
    order_form.save()
    return simplejson.dumps({})

@dajaxice_register
def saveExecuteTechRequire(request,execute_id,content):
    materiel_execute=MaterielExecute.objects.get(document_number=execute_id)
    materiel_execute.tech_requirement=content
    materiel_execute.save()
    return simplejson.dumps({})
@dajaxice_register
def selectEntryType(request,bid,selected,selectentryform):
    entrytypedict = dict(list(STORAGE_ENTRY_TYPECHOICES))
    selectform = EntryTypeForm(deserialize_form(selectentryform))
    if selectform.is_valid() :
        selectvalue = selectform.cleaned_data["entry_type"]
        items_set = getArrivalInspections(selected)
        html = render_to_string("purchasing/addentryitems.html",{"items":items_set,"entrytype":entrytypedict[int(selectvalue)]})
        return simplejson.dumps({"html":html,"items_set":selected,"selectvalue":selectvalue,"bid":bid})

@dajaxice_register
def genEntry(request,items_set,bid):
    items_set = getArrivalInspections(items_set)
    try:
        bidform = BidForm.objects.get(bid_id = bid)
        entry_factory = AutoGenEntry(request.user,items_set,bidform)
        isOk = True
    except Exception,e:
        isOk = False
        print e
    cargo_set = ArrivalInspection.objects.filter(bidform__bid_id = bid,check_pass = False)
    html = render_to_string("purchasing/widgets/arrivalinspection_table.html",{"cargo_set":cargo_set})
    return simplejson.dumps({"html":html,"isOk":isOk})


def getArrivalInspections(selected_id_set):
    items_set = []
    for itemid in selected_id_set:
        try:
            item = ArrivalInspection.objects.get(id=itemid)
            items_set.append(item)
        except Exception,e:
            print e
    return items_set


def getEntryDataModel(selectvalue):
    selectvalue = int(selectvalue)
    if selectvalue == STORAGE_ENTRY_TYPE_WELD:
        entrymodel = WeldMaterialEntry
        entryitemmodel = WeldMaterialEntryItems
    return entrymodel,entryitemmodel


@dajaxice_register
def orderformToExecute(request,orderform_id):
    executeForm=MaterielExecuteForm()
    html=render_to_string("purchasing/materielexecute/widget/materielexecute_view_form.html",{"executeForm":executeForm})
    return simplejson.dumps({"html":html})

@dajaxice_register
#@transaction.commit_manually
def saveOrderformExecute(request,orderform_id,form):
    orderform=OrderForm.objects.get(order_id=orderform_id)
    materielExecuteForm=MaterielExecuteForm(deserialize_form(form))
    print materielExecuteForm
    if materielExecuteForm.is_valid():
        try:
            materielexecute = MaterielExecute();
            materielexecute.document_number = materielExecuteForm.cleaned_data["document_number"]
            materielexecute.materiel_choice = materielExecuteForm.cleaned_data["materiel_choice"]
            materielexecute.document_lister = request.user
            materielexecute.date = datetime.today()
            materielexecute.is_save = False
            materielexecute.save()
            orderform.meterielexecute=materielexecute
            orderform.save()
            for item in orderform.materielformconnection_set.all():
                materiel=item.materiel
                materielexecutedetail=MaterielExecuteDetail(materiel_execute=materielexecute,materiel=materiel)
                materielexecutedetail.save()
                ret={'status':'0','message':u"材料执行表保存成功！"}
        except:
            transaction.rollback()
            ret={'status':'1','message':u"材料执行表保存失败！"}
    else:
        print "sss"
        ret={'status':'1','message':u'材料执行保存失败!'}
    return simplejson.dumps(ret)
@dajaxice_register
def entryConfirmQuery(request,entry_select):
    #Liuguochao

    replace_dic = {}
    filter_dic = {"entry_status":STORAGESTATUS_PURCHASER}
    if entry_select == "1":
        _Model = WeldMaterialEntry
    elif entry_select == "2":
        _Model = SteelMaterialPurchasingEntry
        replace_dic = {"entry_code":"form_code",}
    elif entry_select == "3":
        _Model = AuxiliaryToolEntryCardList
        replace_dic = {"entry_status":"status","entry_time":"create_time","entry_code":"index"}
        filter_dic = {"status":STORAGESTATUS_PURCHASER,}
    elif entry_select == "4":
        _Model = OutsideStandardEntry
    html = handleProcess(_Model,filter_dic,entry_select, replace_dic)
    data = {
        "html":html,
    }
    return simplejson.dumps(data)

def handleProcess(_Model,filter_dic,entry_select,replace_dic = None):
    entry_set = _Model.objects.filter(**filter_dic)
    for item in entry_set:
        if replace_dic != None:
            for k,v in replace_dic.items():
                setattr(item,k,getattr(item,v))
    entry_set.order_by("-entry_time")
    html = render_to_string("purchasing/widgets/purchasing_entry_table.html",{'entry_set':entry_set,
                "entryurl":"arrivalInspectionConfirm","STORAGESTATUS_PURCHASER":STORAGESTATUS_PURCHASER,
                "entry_type":entry_select})
    return html
@dajaxice_register
def entryInspectionConfirm(request,eid,entry_typeid):
    entry_typeid = int(entry_typeid)
    if entry_typeid == 1:
        message = handleEntryInspectionConfirm(request,WeldMaterialEntry,eid,entry_typeid)
    elif entry_typeid == 2:
        message = handleEntryInspectionConfirm(request,SteelMaterialPurchasingEntry,eid,entry_typeid)
    elif entry_typeid == 3:
        message = handleEntryInspectionConfirm(request,AuxiliaryToolEntryCardList,eid,entry_typeid)
    elif entry_typeid == 4:
        message = handleEntryInspectionConfirm(request,OutsideStandardEntry,eid,entry_typeid)
    return message
def handleEntryInspectionConfirm(request,_Model,eid,entry_typeid):
    entry = _Model.objects.get(id = eid)
    status = entry.status if entry_typeid == 3 else entry.entry_status
    if status == STORAGESTATUS_PURCHASER:
        if entry_typeid == 3:
            entry.status = STORAGESTATUS_KEEPER
        else:
            entry.entry_status = STORAGESTATUS_KEEPER
        entry.purchaser = request.user
        entry.save()
        flag = True
    else:
        flag = False
    return simplejson.dumps({'flag':flag})

@dajaxice_register
def getMergeForm(request,pendingArray):
    items_merge = [Materiel.objects.get(id = id) for id in pendingArray]
    order_form=OrderFormForm()
    for field in order_form:
        if field.name == "remark":
            value =""
            for item in items_merge:
                value=value+item.index+"#"
            order_form.initial[field.name]=value
        else:
            value=getattr(items_merge[0],field.name)
            flag=True
            for item in items_merge:
                if value != getattr(item,field.name):
                    flag=False
            if flag:
                order_form.initial[field.name]=value
    count=0
    purchasing=0
    for item in items_merge:
        count=count+(int(item.materielformconnection.count) if item.materielformconnection.count else 0)
        purchasing=purchasing+(float(item.materielformconnection.purchasing) if item.materielformconnection.purchasing else 0)
        form_html = render_to_string("purchasing/orderform/order_form.html",{'order_form':order_form,'count':count,'purchasing':purchasing})
    return simplejson.dumps({'form':form_html})


@dajaxice_register
def MergeMateriel(request,order_id,form,pendingArray,count,purchasing):
    new_form=OrderFormForm(deserialize_form(form))
    new_materiel=new_form.save(commit=False);
    items_materiel= [Materiel.objects.get(id = id) for id in pendingArray]
    new_materiel.inventory_type=items_materiel[0].inventory_type
    new_materiel.save()
    work_order=[]
    for item in items_materiel:
        item.relate_material=new_materiel
        item.save()
        item.materielformconnection.order_form=None
        #item.materielformconnection.count=count
        #item.materielformconnection.purchasing=purchasing
        item.materielformconnection.save()
        if item.work_order:
            item_work=item.work_order.split(',')
            print item_work
            work_order=work_order+item_work
    work_order=set(work_order)
    new_materiel.work_order=','.join(work_order)
    new_materiel.save()
    order_form=OrderForm.objects.get(order_id=order_id)
    mfc= MaterielFormConnection(materiel=new_materiel,order_form=order_form)
    mfc.count=count
    mfc.purchasing=purchasing
    mfc.save()
    status=u'合并成功'
    return simplejson.dumps({'status':status})

@dajaxice_register
def GoToBid(request,index):
    bid_status = BidFormStatus.objects.get(part_status = BIDFORM_PART_STATUS_SELECT_SUPPLLER_APPROVED)
    bid_form = BidForm(
        bid_id = "2016%05d" % (getMaxId(BidForm) + 1),
        bid_status = bid_status,
    )
    bid_form.order_form=OrderForm.objects.get(order_id=index)
    bid_form.save()
    return simplejson.dumps({})

@dajaxice_register
def BidApplySelect(request,val,bidid):
    bidform=BidForm.objects.get(bid_id=bidid)
    bidform.bid_mod=int(val)
    bidform.save()
    goNextStatus(bidform,request.user)
    return simplejson.dumps({})

@dajaxice_register
def BidApplyComment(request,bid_apply_id,usertitle,comment):
    bid_apply=bidApply.objects.get(id=bid_apply_id)
    bid_comment=BidComment(user=request.user,comment=comment,bid=bid_apply.bid,submit_date=datetime.today(),user_title=usertitle)
    bid_comment.save()
    BidNextStatus(bid_apply)
    return simplejson.dumps({})

@dajaxice_register
def BidApplyLogistical(request,form,bid_apply_id,usertitle):
    bid_apply=bidApply.objects.get(pk=bid_apply_id)
    bid_logistical_form = BidLogisticalForm(deserialize_form(form), instance=bid_apply)
    if bid_logistical_form.is_valid():
        bid_logistical_form.save()
    else :
        return simplejson.dumps({'status':1})
    bid_comment=BidComment(user=request.user,comment="",bid=bid_apply.bid,submit_date=datetime.today(),user_title=usertitle)
    bid_comment.save()
    BidNextStatus(bid_apply)
    return simplejson.dumps({'status':0})

@dajaxice_register
def saveSupplierCheck(request,form,supplier_check_id,supplier_form_set,supplier_id_set):
    supplier_check=SupplierCheck.objects.get(pk=supplier_check_id)
    supplier_check_form=SupplierCheckForm(deserialize_form(form),instance=supplier_check)
    if supplier_check_form.is_valid():
        supplier_check_form.save()
    else:
        for item in  supplier_check_form.errors.keys():
            print item,supplier_check_form.errors[item]
        return simplejson.dumps({'status':1})
    for (id,form) in zip(supplier_id_set,supplier_form_set):
        supplierselect=SupplierSelect.objects.get(pk=id)
        form=SupplierCheckSupplierForm(deserialize_form(form),instance=supplierselect)
        form.save()
    return simplejson.dumps({"status":0})



