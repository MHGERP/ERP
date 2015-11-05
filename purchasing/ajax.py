# coding: UTF-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from purchasing.models import *
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
from purchasing.forms import SupplierForm,ProcessFollowingForm,SubApplyItemForm, MaterielExecuteForm
from django.db.models import Q
from datetime import datetime
from purchasing.utility import goNextStatus,goStopStatus,buildArrivalItems

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
    bidform = cargo_obj.bidform
    if PurchasingEntry.objects.filter(bidform = bidform).count() == 0:
        val = not val
        setattr(cargo_obj,arrivalfield,val)
        cargo_obj.save()
        val = getattr(cargo_obj,arrivalfield)
        message = u"状态修改成功"
        isOk = True
    else:
        message = u"状态修改失败，入库单已经存在"
        isOk = False
    data = {
        "flag":val, 
        "message":message,
        'isOk':isOk,
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
            goNextStatus(bidform,request.user)
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
    """
    Lei
    """
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
    for item in items:
        if MaterielFormConnection.objects.filter(materiel = item).count() == 0:
            MaterielFormConnection(materiel = item, count = item.count).save()
        
        if item.inventory_type.id <= 2 :
            if item.materielexecutedetail_set.count()>0:
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
        detailForm = MainMaterielExecuteDetailForm()
        materielexecute_detail_html = "purchasing/materielexecute/table/main_materielexecute_detail_table.html"
        #formname = "MainMaterielExecuteDetailForm"
        add_form = render_to_string("purchasing/materielexecute/widget/add_main_detail_form.html", {"MainMaterielExecuteDetailForm":detailForm})
        current_materiel_choice = MATERIEL_CHOICE[0][1]
    else:
        # materielexecute_detail_set = SupportMaterielExecuteDetail.objects.all()
        detailForm = SupportMaterielExecuteDetailForm()
        materielexecute_detail_html = "purchasing/materielexecute/table/support_materielexecute_detail_table.html"
        #formname = "SupportMaterielExecuteDetailForm"
        add_form = render_to_string("purchasing/materielexecute/widget/add_support_detail_form.html", {"SupportMaterielExecuteDetailForm":detailForm})
        current_materiel_choice = MATERIEL_CHOICE[1][1]
    # choice_form = MaterielChoiceForm()
    context = {
        "choice" : SUPPORT_MATERIEL,
        "MAIN_MATERIEL" : MAIN_MATERIEL
        # "materielChoice_form" : choice_form,
        #formname : detailForm
    }

    rendered_materielexecute_detail_html = render_to_string(materielexecute_detail_html, context)
    return simplejson.dumps({'materielexecute_detail_html' : rendered_materielexecute_detail_html, 'add_form' : add_form, 'current_materiel_choice' : current_materiel_choice})

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
@transaction.commit_manually
def saveMaterielExecuteDetail(request, form, materielChoice):
    """
    mxl
    summary : save the materielExecute and MainMaterielExecuteDetail(SupportMaterielExecuteDetail) models
    params : form : the submit form(detail)
             documentNumberInput : document_number of MaterielExecute model
             materielChoice : materielChoice of  MaterielExecute model
    """
    flag = False;
    try:
        # materielexecute = MaterielExecute();
        # materielexecute.document_number = documentNumberInput
        # materielexecute.document_lister = request.user
        # materielexecute.date = datetime.today()

        if materielChoice == MAIN_MATERIEL:
            # materielexecute.materiel_choice = MATERIEL_CHOICE[0][0]
            detail_Form = MainMaterielExecuteDetailForm(deserialize_form(form))
            if detail_Form.is_valid():
                materielexecute_detail = detail_Form.save()
                flag = True

        else:
            # materielexecute.materiel_choice = MATERIEL_CHOICE[1][0]
            detail_Form = SupportMaterielExecuteDetailForm(deserialize_form(form))
            if detail_Form.is_valid():
                materielexecute_detail = detail_Form.save()
                flag = True

        if flag:
            # materielexecute.save()
            # print materielexecute.materiel_choice
            # materielexecute_detail.materiel_execute = materielexecute
            materielexecute_detail.save()
            materielexecute_detail_set = [materielexecute_detail]
    except Exception, e:
        transaction.rollback()
        print e
    if flag:
        transaction.commit()
        if materielChoice == MAIN_MATERIEL:
            detail_table = render_to_string("purchasing/materielexecute/table/main_td.html", {"materielexecute_detail_set" : materielexecute_detail_set})
        else:
            detail_table = render_to_string("purchasing/materielexecute/table/support_td.html", {"materielexecute_detail_set" : materielexecute_detail_set})
        ret = {'status' : '1', 'message' : u'保存成功', 'detail_table' : detail_table, 'materielexecute_detail_id' : materielexecute_detail.id}
    else:
        # errorsFiled = render_to_string("purchasing/materielexecute/widget/errorsField.html", {"errorsFiled" : detail_Form})
        if materielChoice == MAIN_MATERIEL:
            add_form = render_to_string("purchasing/materielexecute/widget/add_main_detail_form.html", {"MainMaterielExecuteDetailForm":detail_Form})
        else:
            add_form = render_to_string("purchasing/materielexecute/widget/add_support_detail_form.html", {"SupportMaterielExecuteDetailForm":detail_Form})
        ret = {'status' : '0', 'message' : u'请检查输入是否正确', 'add_form' : add_form}
        transaction.rollback()
    return simplejson.dumps(ret)

@dajaxice_register
def materielExecuteCommit(request, detail_id_array, materielChoice, materielExecuteId):
    try:
        print materielExecuteId
        materielExecute = MaterielExecute.objects.get(id=materielExecuteId)
        materielExecute.is_save = True
        if materielChoice == MAIN_MATERIEL:
            for detail_id in detail_id_array:
                print detail_id
                mainMaterielExecuteDetail = MainMaterielExecuteDetail.objects.get(id=detail_id)
                mainMaterielExecuteDetail.materiel_execute = materielExecute
                mainMaterielExecuteDetail.save()
        else:
            for detail_id in detail_id_array:
                print detail_id
                supportMaterielExecuteDetail = SupportMaterielExecuteDetail.objects.get(id=detail_id)
                supportMaterielExecuteDetail.materiel_execute = materielExecute
                supportMaterielExecuteDetail.save()
        materielExecute.save()
        ret = {'status' : '1'}
    except Exception, e:
        ret = {'status' : '0'}
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
def saveBidApply(request, form, bid_id):
    bidform = BidForm.objects.get(id = bid_id)
    try:
        bidapply = bidApply.objects.get(bid = bidform)
        bidApplyForm = BidApplyForm(deserialize_form(form), instance=bidapply)
    except:
        bidapply = None
        bidApplyForm = BidApplyForm(deserialize_form(form))
    if bidApplyForm.is_valid():
        if bidapply:
            bidApplyForm.save()
        else:
            bidapply = bidApplyForm.save(commit = False)
            bidapply.bid = bidform
            bidapply.save()
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
def submitStatus(request, bid_id):
    try:
        bidform = BidForm.objects.get(id = bid_id)
        goNextStatus(bidform, request.user)
        ret = {'status': '1', 'message': u"申请书提交成功"}
    except:
        ret = {'status': '2', 'message': u"申请书不存在"}
    return simplejson.dumps(ret)
    

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
    for item in items:
        item.can_choose, item.status = (False, u"已加入标单") if (item.materielformconnection.bid_form != None) else (True, u"未加入标单")

    context = {
        "items": items,
        "can_choose": can_choose,
    }
    html = render_to_string("purchasing/orderform/orderform_item_list.html", context)
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
def getOngoingOrderList(request):
    """
    Lei
    """
    order_form_list = OrderForm.objects.filter(Q(order_status__status = 0))
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
def newOrderCreate(request):
    """
    Lei
    """
    cDate_datetime = datetime.now()
    order_status = OrderFormStatus.objects.get(status = 0)
    order_form = OrderForm(
        order_id = "2015%05d" % (getMaxId(OrderForm) + 1),
        create_time = cDate_datetime,
        order_status = order_status,
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
        if materiel.inventory_type.id <= 2:
            addToExecute(materiel)
        try:
            conn = MaterielFormConnection.objects.get(materiel = materiel)
        except:
            conn = MaterielFormConnection(materiel = materiel)
        conn.order_form = order_form
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
        item.status = u"已加入"

    items_pending = [Materiel.objects.get(id = id) for id in pendingArray]
    for item in items_pending:
        item.status = u"待加入"

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
        item.status = u"已加入"

    items_pending = [Materiel.objects.get(id = id) for id in pendingArray]
    for item in items_pending:
        item.status = u"待加入"

    html = render_to_string("purchasing/orderform/orderform_item_list.html", {"items": items, "can_choose": False, "items_pending": items_pending, })
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

def addToExecute(materiel):
    materiel_execute_detail=MaterielExecuteDetail(materiel=materiel)
    materiel_execute_detail.save()



@dajaxice_register
def AddToMaterialExecute(request,selected):
    for item in selected:
        materiel=Materiel.objects.get(pk=item)
        addToExecute(materiel)

