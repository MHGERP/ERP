# coding: UTF-8
import datetime
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from const import *
from const.models import Materiel,OrderFormStatus, BidFormStatus
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib.auth.models import User
from django.db import transaction 
from const.models import WorkOrder, Materiel
from const.forms import InventoryTypeForm
from const import *
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q,F
from datetime import datetime
from storage.models import *
from storage.forms import *
from storage.utils import *
from django.shortcuts import render
from operator import attrgetter
@dajaxice_register
def get_apply_card_detail(request,apply_card_index):
    context={}
    return render(request,'storage/weldapply/weldapplycarddetail.html',context)

@dajaxice_register
def searchApplyCard(request,form):
    """
    author: Rosen
    summary:process the search request for steel apply card and return the result
    params: search form
    return: search result and message
    """
    form = SteelApplyCardSearchForm(deserialize_form(form))
    context={}
    if form.is_valid():
        steel_apply_cards = get_weld_filter(SteelMaterialApplyCard,form.cleaned_data)
        result_table = render_to_string("storage/widgets/apply_card_table.html",{"apply_cards":steel_apply_cards})
        message = "success"
        context["result_table"]=result_table
    else:
        message = "errors"
    context["message"]=message
    return simplejson.dumps(context)

@dajaxice_register
def searchRefundCard(request,form):
    """
    author: Rosen
    summary:process the search request for steel refund card and return the result
    params: search form
    return: search result and message
    """
    form = SteelRefundSearchForm(deserialize_form(form))
    context={}
    if form.is_valid():
        conditions = form.cleaned_data
        steel_refund_cards = get_weld_filter(CommonSteelMaterialReturnCardInfo,conditions)
        print steel_refund_cards
        result_table = render_to_string("storage/widgets/refund_card_table.html",{"refund_cards":steel_refund_cards})
        message = "success"
        context["result_table"]=result_table
    else:
        message = "errors"
    context["message"]=message
    return simplejson.dumps(context)

@dajaxice_register
def searchSteelLedger(request,form):
    """
    author: Rosen
    summary:process the search request for steel ledger and return the result
    params: search form
    return: search result and message
    """
    form = SteelLedgerSearchForm(deserialize_form(form))
    context={}
    if form.is_valid():
        conditions = form.cleaned_data
        steel_set = get_weld_filter(SteelMaterial,conditions)
        print steel_set
        result_table = render_to_string("storage/widgets/steel_ledger_table.html",{"steel_set":steel_set})
        message = "success"
        context["result_table"]=result_table
    else:
        message = "errors"
    context["message"]=message
    return simplejson.dumps(context)

@dajaxice_register
def steelApplyEnsure(request,form_code):
    """
    Author:Rosen
    Summay:钢材领用确认
    Params:钢材领用单编号
    return:提示信息
    """
    common_steelapply = CommonSteelMaterialApplyCardInfo.objects.get(form_code=form_code)
    if common_steelapply.steel_type==BOARD_STEEL:message=boardSteelApplyEnsure(request,common_steelapply)
    if common_steelapply.steel_type==BAR_STEEL:message=barSteelApplyEnsure(request,common_steelapply)
    return message
def barSteelApplyEnsure(request,common_card):
    """
    Author:Rosen
    Summay:型材领用确认
    Params:领用单表头
    return:提示信息
    """
    steel_set = common_card.barsteelmaterialapplycardcontent_set.all()
    for steel in steel_set:
        quantity_ledger = steel.steel_material.barsteelmaterialledger.quantity
        quantity_need = steel.quantity
        if quantity_need > quantity_ledger:return u"%s(%s)库存不足"%(steel.steel_material.name,steel.steel_material.specifications) 

    for steel in steel_set:
        ledger = steel.steel_material.barsteelmaterialledger
        ledger.quantity = ledger.quantity - steel.quantity
        ledger.save()

    common_card.apply_confirm=True
    common_card.save()

    return u"领用成功"

def boardSteelApplyEnsure(request,common_card):
    """
    Author:Rosen
    Summay:板材领用确认
    Params:领用单表头
    return:提示信息
    """
    steel_set = common_card.boardsteelmaterialapplycardcontent_set.all()
    for steel in steel_set:
        quantity_ledger=steel.steel_material.boardsteelmaterialledger.quantity
        quantity_need=steel.quantity
        if quantity_need > quantity_ledger:return u"%s(%s)库存不足"%(steel.steel_material.name,steel.steel_material.specifications)
    for steel in steel_set:
        ledger = steel.steel_material.boardsteelmaterialledger
        ledger.quantity=ledger.quantity - steel.quantity
        ledger.save()

    common_card.apply_confirm = True
    common_card.save()

    return u"领用成功"


@dajaxice_register
def steelRefundEnsure(request,form_code):
    """
    kad
    """
    common_refund = CommonSteelMaterialReturnCardInfo.objects.get(form_code = form_code)
    if common_refund.steel_type == BOARD_STEEL:
        message = boardSteelRefundEnsure(request, common_refund)
    elif common_refund.steel_type == BAR_STEEL:
        message = barSteelRefundEnsure(request, common_refund)
    return message

def boardSteelRefundEnsure(request, common_refund):
    """
    kad
    """
    refund_set = common_refund.boardsteelmaterialreturncardcontent_set.all()
    for refund in refund_set:
        refund_quantity = refund.quantity
        refund_matnum = refund.steel_material.material_number
        ledger = SteelMaterial.objects.get(material_number = refund_matnum)
        ledger_quantity = ledger.boardsteelmaterialledger.quantity
        ledger_quantity += refund_quantity
        ledger.boardsteelmaterialledger.quantity = ledger_quantity
        ledger.boardsteelmaterialledger.save()
        ledger_returntime = ledger.return_time
        ledger_returntime += 1
        ledger.return_time = ledger_returntime
        ledger.save()
    common_refund.return_confirm = True
    common_refund.save()
    return u"退库成功"

def barSteelRefundEnsure(request, common_refund):
    """
    kad
    """
    refund_set = common_refund.barsteelmaterialreturncardcontent_set.all()
    for refund in refund_set:
        refund_quantity = refund.quantity
        refund_matnum = refund.steel_material.material_number
        ledger = SteelMaterial.objects.get(material_number = refund_matnum)
        ledger_quantity = ledger.barsteelmaterialledger.quantity
        ledger_quantity += refund_quantity
        ledger.barsteelmaterialledger.quantity = ledger_quantity
        ledger.barsteelmaterialledger.save()
        ledger_returntime = ledger.return_time
        ledger_returntime += 1
        ledger.return_time = ledger_returntime
        ledger.save()
    common_refund.return_confirm = True
    common_refund.save()
    return u"退库成功"

@dajaxice_register
def storeRoomSearch(request, form):
    """
    kad
    """
    search_form = StoreRoomSearchForm(deserialize_form(form))
    if search_form.is_valid():
        room_set = get_weld_filter(StoreRoom,search_form.cleaned_data)
        html = render_to_string("storage/widgets/storeroom_table.html",{"room_set":room_set})
    else:
        print search_form.errors
    data = {
        "html":html,
    }
    return simplejson.dumps(data)

@dajaxice_register
def storeRoomAdd(request, form):
    """
    kad
    """
    room_form = StoreRoomForm(deserialize_form(form))
    if room_form.is_valid():
        room_form.save()
        message = u"录入成功"
        flag = True
    else: 
        message = u"录入失败"
        flag = False
    room_set = StoreRoom.objects.all().order_by('-id')
    html = render_to_string("storage/widgets/storeroom_table.html", {"room_set":room_set})
    data = {
        "message":message,
        "html":html,
        "flag":flag,
    }
    return simplejson.dumps(data) 

@dajaxice_register
def storeRoomUpdate(request, form, sr_id):
    """
    kad
    """
    room_obj = StoreRoom.objects.get(id = sr_id)
    room_form = StoreRoomForm(deserialize_form(form), instance = room_obj)
    if room_form.is_valid():
        #room_form.save(commit = False)
        room_form.save()
        message = u"修改成功"
        flag = True
    else:
        message = u"修改失败"
        flag = False
    room_set = StoreRoom.objects.all().order_by('-id')
    html = render_to_string("storage/widgets/storeroom_table.html", {"room_set":room_set})
    data = {
        "message":message,
        "html":html,
        "flag":flag,
    }
    return simplejson.dumps(data)
   
@dajaxice_register
def storeRoomDelete(request, sr_id):
    """
    kad
    """
    try:
        room_obj = StoreRoom.objects.get(id = sr_id)
        room_obj.delete()
        message = u"删除成功"
        flag = True
    except Exception,e:
        print e
        message = u"删除失败"
        flag = False
    data = {
        "message":message,
        "flag":flag,
        "sr_id":sr_id,
    }
    return simplejson.dumps(data)

@dajaxice_register
def auEntryUpdate(request, aid, remark):
    """
    kad
    """
    item = AuxiliaryToolEntryItems.objects.get(id = aid);
    item.remark = remark;
    item.save();
    message = u"修改成功"
    data = {
        "message":message,
        "aid":aid,
        "remark":remark,
    }
    return simplejson.dumps(data);

@dajaxice_register
def auToolEntryConfirm(request, role, eid):
    try:
        entry = AuxiliaryToolEntry.objects.get(id = eid);
        if role == "keeper":
            if entry.entry_status == STORAGESTATUS_KEEPER:
                entry.keeper = request.user;
                entry.entry_status = STORAGESTATUS_END;
                entry.save();
                createAuxiliaryToolStoreList(entry)
                message = u"入库单确认成功";
            else:
                message = u"入库单已经确认过，不能重复确认";
    except Exception,e:
        print e
        message = u"入库单不存在";
    entry = AuxiliaryToolEntry.objects.get(id = eid);
    items = AuxiliaryToolEntryItems.objects.filter(entry = entry);
    html = render_to_string("storage/wordhtml/auxiliaryToolEntryTable.html", {"items":items, "entry":entry});
    data = {
        "html":html,
        "message":message,
    }
    return simplejson.dumps(data);




@dajaxice_register
def Search_History_Apply_Records(request,data):
    context={}
    context['APPLYCARD_KEEPER']=APPLYCARD_KEEPER
    form=ApplyCardHistorySearchForm(deserialize_form(data))
    if form.is_valid():
        context['apply_cards']=get_weld_filter(WeldingMaterialApplyCard,form.cleaned_data)
        return render_to_string('storage/weldapply/history_table.html',context)

@dajaxice_register
def Auxiliary_Detail_Query(request,id):
    context={}
    object_id=int(id)
    auxiliary_tool=AuxiliaryTool.objects.get(id=object_id)
    context['model']=dict(AUXILIARY_TOOLS_MODELS_CHOICES)[int(auxiliary_tool.model)]
    context['measurement_unit']=auxiliary_tool.measurement_unit
    context['unit_price']=auxiliary_tool.unit_price
    return HttpResponse(simplejson.dumps(context))


@dajaxice_register
def Auxiliary_Tools_Apply_Create(request,data):
    ins=None
    form_data = deserialize_form(data)
    apply_card=AuxiliaryToolsCardCommitForm(form_data,instance=ins)
    save_ins=apply_card.save(commit=False)
    save_ins.applicant=request.user
    save_ins.status=AUXILIARY_TOOL_APPLY_CARD_APPLYED
    save_ins.save()
    return HttpResponse('[SUCCESS] create apply card succeed')


@dajaxice_register
def Auxiliary_Tools_Apply_Commit(request,data):
    form_data = deserialize_form(data)
    ins_index=int(form_data['index'])
    if ins_index!=0:
        try:
            ins=AuxiliaryToolApplyCard.objects.get(index=ins_index)
        except:
            return HttpResponse('[ERROR] no such instance')
    else:
        Auxiliary_Tools_Apply_Create(request,data)
    apply_card=AuxiliaryToolsCardCommitForm(form_data,instance=ins)
    if apply_card.is_valid():
        save_ins=apply_card.save(commit=False)
        if ins_index!=0:
            save_ins.commit_user=request.user
        else:
            save_ins.applicant=request.user
        if save_ins.actual_item.quantity < save_ins.actual_quantity:
            return HttpResponse("[ERROR] quantity error")
        save_ins.actual_total=save_ins.actual_item.unit_price*save_ins.actual_quantity
        print save_ins.actual_quantity
        save_ins.actual_item.quantity-=save_ins.actual_quantity
        save_ins.actual_item.save()
        save_ins.status=AUXILIARY_TOOL_APPLY_CARD_COMMITED
        save_ins.save()
    else:
        print apply_card.errors
    return HttpResponse('[SUCCESS] commit apply card succeed')

@dajaxice_register
def Auxiliary_Tools_Entry(request,data):
    form_data = deserialize_form(data)
    object_id = int(form_data['object_id'])
    auxiliary_card_list = AuxiliaryToolEntryCardList.objects.get(id=object_id)
    auxiliarytools = AuxiliaryToolEntryCard.objects.filter(card_list__id=object_id)
    for at in auxiliarytools:
        if at.quantity<0:
            return HttpResponse('[ERROR]Auxiliary tools entry quantity error')
        at.auxiliary_tool.quantity=F('quantity')+at.quantity
    for at in auxiliarytools:
        at.auxiliary_tool.save()
    auxiliary_card_list.status=STORAGESTATUS_END
    auxiliary_card_list.keeper=request.user
    auxiliary_card_list.save()
    return HttpResponse('[SUCCESS] entry succeed')
 

@dajaxice_register
def Search_Auxiliary_Tools_Records(request,data,search_type):
    context={}
    form=AuxiliaryToolsSearchForm(deserialize_form(data))
    if form.is_valid():
        conditions=form.cleaned_data
        if search_type=='inventory':
            context['rets'] = get_weld_filter(AuxiliaryToolStoreList,conditions)
            return render_to_string('storage/auxiliarytools/inventory_table.html',context)
        else:
            if search_type=='apply':
                context['rets']=get_weld_filter(AuxiliaryToolApplyCard,conditions)
                return render_to_string('storage/auxiliarytools/apply_table.html',context)

@dajaxice_register
def Search_Auxiliary_Tools_Apply_Card(request,data):
    context={}
    print data
    form=AuxiliaryToolsApplyCardSearchForm(deserialize_form(data))
    if form.is_valid():
        conditions=form.cleaned_data
        print conditions
        context['apply_cards']=get_weld_filter(AuxiliaryToolApplyCard,conditions)
        print context['apply_cards']
    else:
        print form.errors
    return render_to_string('storage/auxiliarytools/apply_card_table.html',context)    

"""
@dajaxice_register
def weldhum_insert(request,hum_params):
    hum_params=deserialize_form(hum_params)
    form = HumRecordForm(hum_params)
    if form.is_valid():
        form.save()
        message = u"录入成功"
        flag = True
    else:
        flag = False
        message = u"录入失败"

    html = render_to_string("storage/widgets/humiture_form.html",{"form":form,})
    data = {
        "flag":flag,
        "html":html,
        "message":message,
    }
    return simplejson.dumps(data)
"""


@dajaxice_register
def entryItemSave(request,form,mid):
    item = WeldMaterialEntryItems.objects.get(id = mid)
    entry_form = EntryItemsForm(deserialize_form(form),instance = item) 
    entry = item.entry
    flag = False
    if entry.auth_status(STORAGESTATUS_KEEPER):
        if entry_form.is_valid():
            entry_form.save()
            flag = True
            message = u"修改成功"
        else:
            print entry_form.errors
            message = u"修改失败"
    else:
        message = u"修改失败，入库单已确认过"
    is_show = entry.entry_status == STORAGESTATUS_KEEPER
    items = WeldMaterialEntryItems.objects.filter(entry = entry)
    html = render_to_string("storage/wordhtml/weldentryitemstable.html",{"items":items,"is_show":is_show,"entry":entry})
    data = {
            "flag":flag,
            "message":message,
            "html":html,
           }
    return simplejson.dumps(data)

@dajaxice_register
def saveSteelEntryStoreRoom(request,form,mid):
    form = steelEntryItemsForm(deserialize_form(form))
    item = SteelMaterialEntryItems.objects.get(id = mid)
    entry = item.entry
    items = entry.steelmaterialentryitems_set.all()
    if form.is_valid():
        storeroom_id = form.cleaned_data['store_room']
        store_room = StoreRoom.objects.get(id = storeroom_id)
        if entry.entry_status == STORAGESTATUS_KEEPER:
            item.store_room = store_room
            item.save()
            message = u"修改成功"
        else:
            message = u"修改失败，入库单已确认过"
    html = render_to_string("storage/wordhtml/steelentryitems.html",{"entry":entry,"items":items})
    data = {
        "message":message,
        "html":html,
    }
    return simplejson.dumps(data)

@dajaxice_register
def saveSteelEntryRemark(request,form,eid):
    entry = SteelMaterialEntry.objects.get(id = eid)
    form = steelEntryRemarkForm(deserialize_form(form),instance=entry)
    items = entry.steelmaterialentryitems_set.all() 
    if form.is_valid():
        if entry.entry_status == STORAGESTATUS_KEEPER:
            form.save()
            message = u"修改成功"
        else:
            message = u"修改失败，入库单已确认过"
            
    html = render_to_string("storage/wordhtml/steelentry.html",{"entry":entry,"items":items,"BAR_STEEL":BAR_STEEL})
    data = {
        "message":message,
        "html":html,
    }
    return simplejson.dumps(data)

@dajaxice_register
def entryConfirm(request,role,eid):
    data = {}
    try:
        entry = WeldMaterialEntry.objects.get(id = eid)
        if role == "keeper":
            data,is_show = handleEntryConfirm_Keeper(request,entry)
    except Exception,e:
        print e
        data["message"] = u"入库单不存在"
    items = entry.weldmaterialentryitems_set.all()
    html = render_to_string("storage/wordhtml/weldentryitemstable.html",{"items":items,"is_show":is_show,"entry":entry})
    data["html"] = html
    data["role"] = role
    return simplejson.dumps(data)    

def handleEntryConfirm_Keeper(request,entry):
    if entry.entry_status == STORAGESTATUS_KEEPER:
        entry.keeper = request.user
        entry.entry_status = STORAGESTATUS_END
        entry.save()
        weldStoreItemsCreate(entry)
        message = u"入库单确认成功"
    else:
        message = u"入库单已经确认过,不能重复确认"
    is_show = entry.entry_status == STORAGESTATUS_KEEPER 
    return {"message":message},is_show

@dajaxice_register
def steelEntryConfirm(request,eid,role):
    try:
        entry = SteelMaterialEntry.objects.get(id = eid)
        if role == "keeper": 
            if entry.entry_status == STORAGESTATUS_KEEPER:
                createSteelMaterialStoreList(entry)
                entry.entry_status = STORAGESTATUS_END
                entry.keeper = request.user
                entry.save()
                message =u"入库单确认成功"
            else:
                message = u"入库单已经确认过"
    except Exception,e:
        message = u"入库单确认失败"
        print e
    html = render_to_string("storage/wordhtml/steelentry.html",{"entry":entry,"items":entry.steelmaterialentryitems_set.all(),"BAR_STEEL":BAR_STEEL})
    return simplejson.dumps({'message':message,"html":html})

@dajaxice_register
def getOverTimeItems(request):
    items_set = WeldStoreList.objects.filter(deadline__lt = datetime.date.today() )
    html = render_to_string("storage/widgets/item_table.html",{"items_set":items_set})
    return simplejson.dumps({"html":html})

@dajaxice_register
def getThreadItems(request):
    items_set = WeldStoreList.objects.values("specification").annotate(Sum('count'))
    warning_set = []
    for tmp in items_set:
        try:
            thread = WeldStoreThread.objects.get(specification = tmp["specification"])
            if tmp["count__sum"] < thread.count:
                tmp["count"] = tmp["count__sum"]
                warning_set.append(tmp)
        except Exception,e:
            print e
    html = render_to_string("storage/widgets/item_table.html",{"items_set":warning_set})
    return simplejson.dumps({"html":html})

@dajaxice_register
def storeThreadSave(request,form,mid):
    item = WeldStoreThread.objects.get(id = mid)
    entry_form = ThreadEntryItemsForm(deserialize_form(form),instance = item)
    flag = False
    if entry_form.is_valid():
        entry_form.save()
        flag = True
        message = u"修改成功"
    else:
        message = u"修改失败"
    items_set = WeldStoreThread.objects.all();
    html = render_to_string("storage/widgets/storethread_table.html",{"items_set":items_set})
    data = {
            "flag":flag,
            "message":message,
            "html":html,
           }
    return simplejson.dumps(data)

@dajaxice_register
def storeThreadDelete(request,mid):
    item = WeldStoreThread.objects.get(id = mid)
    item.delete()
    flag = True
    message = u"删除成功"
    items_set = WeldStoreThread.objects.all();
    html = render_to_string("storage/widgets/storethread_table.html",{"items_set":items_set})
    data = {
            "flag":flag,
            "message":message,
            "html":html,
           }
    return simplejson.dumps(data)

@dajaxice_register
def storeThreadAdd(request,form):
    entry_form = ThreadEntryItemsForm(deserialize_form(form))
    if entry_form.is_valid():
        speci = entry_form.cleaned_data['specification']
        is_exist = WeldStoreThread.objects.filter(specification = speci).exists()
        if is_exist:
            message = u"安全量已存在，录入失败"
            flag = False
        else:
            entry_form.save()
            message = u"录入成功"
            flag = True
    else:
        flag = False
        message = u"录入失败"
    items_set = WeldStoreThread.objects.all();
    html = render_to_string("storage/widgets/storethread_table.html",{"items_set":items_set})
    data = {
            "flag":flag,
            "message":message,
            "html":html,
           }
    return simplejson.dumps(data)

@dajaxice_register
def humiChangeSave(request,hidform,hid):
    message = u"修改失败,有未填数据"
    try:
        humi_obj = WeldingMaterialHumitureRecord.objects.get(id=hid)
        form = HumRecordForm(deserialize_form(hidform),instance = humi_obj)
        if form.is_valid():
            humi_obj = form.save(commit = False)
            if humi_obj.date == get_today():
                form.save()
                message = u"修改成功"
    except Exception,e:
        print e
    return simplejson.dumps({"message":message})

@dajaxice_register
def bakeSave(request,bakeform,bid=None):
    weldbake = ""
    if bid != None:
        weldbake = WeldingMaterialBakeRecord.objects.get(id = bid)
    bakeform = deserialize_form(bakeform)
    form = BakeRecordForm(bakeform,instance = weldbake) if bid !=None else BakeRecordForm(bakeform)
    if form.is_valid():
        weldbake = form.save(commit = False)
        weldbake.storeMan = request.user
        weldbake.save()
        message = u"录入成功"
    else:
        message = u"录入失败"
    context = {
               "form":form,
               "weldbake":weldbake,
              }
    html = render_to_string("storage/widgets/bake_form.html",context)
    return simplejson.dumps({"html":html,"message":message})

@dajaxice_register
def outsideEntryConfirm(request,eid,form):
    status_list = [ x[0]  for x in ENTRYSTATUS_CHOICES ] 
    html,flag,context = getEntryData(request,eid,form,OutsideStandardEntry,OutsideStandardItem,StorageOutsideEntryInfoForm,StorageOutsideEntryRemarkForm,"outside/entryhome","keeper",status_list)
    entry_obj = context["entry_obj"]
    items_set = context["entry_set"]
    genOutsideStoreList(items_set)
    if flag:
        message = u"保存成功"
    else:
        message = u"保存失败"
    status_list = [ x[0]  for x in ENTRYSTATUS_CHOICES ] 
    return simplejson.dumps({"html":html,"message":message})

def getEntryData(request,eid,form,_Model,_ItemModel,_Inform,_Reform,entryhomeurl,role,status_list,entry_status=STORAGESTATUS_KEEPER):
    entry_obj = _Model.objects.get(id = eid)
    form = deserialize_form(form)
    inform = _Inform(form,instance=entry_obj)
    reform = _Reform(form,instance=entry_obj)
    form_list = [("inform",inform),("reform",reform)]
    entryobject = EntryObject(status_list,_Model,eid) 
    context = entryobject.save_entry(entry_obj,role,request.user,form_list)
    is_show = entryobject.checkShow(entry_obj,STORAGESTATUS_KEEPER)
    context["entryhomeurl"] = entryhomeurl
    context["is_show"]=is_show
    context["entry_set"] = _ItemModel.objects.filter(entry=entry_obj)
    return render_to_string("storage/widgets/entryAbody.html",context),entryobject.flag,context


def genOutsideStoreList(items_set):
    try:
        for item in items_set:
            storeitem = OutsideStorageList.objects.filter(specification = item.specification,texture = item.materiel.material)
            if storeitem.count() > 0:
                storeitem  = storeitem[0]
                storeitem.number += item.number
                storeitem.save()
            else:
                storeitem = OutsideStorageList(specification = item.specification , texture = item.materiel.material ,number = item.number,unit = item.unit)
                storeitem.save()
        return True
    except Exception,e:
        print e
        return False

@dajaxice_register
def outsideApplyCardItemRemarkChange(request,itemid,remark):
    item = OutsideApplyCardItem.objects.get(id = itemid)
    item.remark = remark
    item.save()
    return simplejson.dumps({"remark":item.remark,"id":item.id})

@dajaxice_register
def outsideApplyCardConfirm(request,form,aid):
    applycard = OutsideApplyCard.objects.get(id = aid)
    form = OutsideApplyCardForm(deserialize_form(form),instance=applycard)
    if form.is_valid():
        form.save()
        saveRolers(applycard,"keeper",request.user)
        items_set = OutsideApplyCardItem.objects.filter(applycard = applycard)
        isOk = updateStorageLits(items_set,OutsideStorageList)
        if isOk:
            message = u"确认成功"
            setObjAttr(applycard,"entry_status",STORAGESTATUS_END)
        else:
            message = u"确认失败，部分材料库存不够"
    else:
        message = u"确认失败，领用单内容未填全"
        print form.errors
    url = "outside/applycardhome"
    default_status = STORAGESTATUS_KEEPER
    context = getOutsideApplyCardContext(applycard,form,url,default_status)
    html = render_to_string("storage/widgets/applycardbody.html",context)
    return simplejson.dumps({"message":message,"html":html})

def getOutsideApplyCardContext(applycard,inform,url,default_status):
    is_show = applycard.entry_status == default_status
    items_set = OutsideApplyCardItem.objects.filter(applycard = applycard)
    context = {
               "inform":inform,
               "applycard":applycard,
               "applycardurl":url,
               "is_show":is_show,
               "items_set":items_set,
              }
    return context

@dajaxice_register
def getOutsideThreadItems(request):
    items_set = OutsideStorageList.objects.all()
    warning_set = []
    for tmp in items_set:
        print tmp
        try:
            thread = WeldStoreThread.objects.get(specification = tmp.specification)
            if tmp.number < thread.count:
                tmp.thread = thread.count
                warning_set.append(tmp)
        except Exception,e:
            print e
    html = render_to_string("storage/widgets/outsidethread_table.html",{"items_set":warning_set})
    return simplejson.dumps({"html":html})

@dajaxice_register
def outsideAccountEntrySearch(request,form):
    form = OutsideAccountEntrySearchForm(deserialize_form(form))
    items_set = {}
    if form.is_valid():
        conditions=form.cleaned_data
        q1=(conditions['date'] and Q(entry__entry_time = conditions['date'])) or None
        q2=(conditions['specification'] and Q(specification=conditions['specification'])) or None
        q3=(conditions['entry_code'] and Q(entry__entry_code=conditions['entry_code'])) or None
        q4=(conditions['work_order'] and Q(materiel__order =conditions['work_order'])) or None
        query_set = filter(lambda x:x!=None,[q1,q2,q3,q4]) 
        if query_set:
            query_conditions=reduce(lambda x,y:x&y,query_set) 
            items_set = OutsideStandardItem.objects.filter(query_conditions)
        else:
            items_set = OutsideStandardItem.objects.all()
        items_set = items_set.filter(entry__entry_status = STORAGESTATUS_END)
    context = {
            'items_set':items_set,
            "search_form":form,
        }
    html = render_to_string("storage/widgets/account/entryhomemain.html",context)
    return simplejson.dumps({"html":html})

@dajaxice_register
def outsideAccountApplyCardSearch(request,form):
    form = OutsideAccountApplyCardSearchForm(deserialize_form(form))
    items_set = {}
    if form.is_valid():
        conditions=form.cleaned_data
        q1=(conditions['date'] and Q(applycard__date = conditions['date'])) or None
        q2=(conditions['specification'] and Q(specification=conditions['specification'])) or None
        q3=(conditions['entry_code'] and Q(applycard__entry_code=conditions['entry_code'])) or None
        q4=(conditions['work_order'] and Q(applycard__workorder =conditions['work_order'])) or None
        q5=(conditions['department'] and Q(department =conditions['department'])) or None
        query_set = filter(lambda x:x!=None,[q1,q2,q3,q4,q5]) 
        if query_set:
            query_conditions=reduce(lambda x,y:x&y,query_set) 
            items_set = OutsideApplyCardItem.objects.filter(query_conditions)
        else:
            items_set = OutsideApplyCardItem.objects.all()
        items_set.filter(applycard__entry_status = STORAGESTATUS_END)
        sorted_items_set = sorted(items_set,key=attrgetter('applycard.workorder.order_index','specification'))
    context = {
            'items_set':sorted_items_set,
            "search_form":form,
        }
    html = render_to_string("storage/widgets/account/applycardhomemain.html",context)
    return simplejson.dumps({"html":html})

@dajaxice_register
def outsideThreadSearch(request,form):
   form = OutsideStorageSearchForm(deserialize_form(form));
   items_set = {}
   if form.is_valid():
       conditions = form.cleaned_data
       print conditions
       q1=(conditions['texture'] and Q(texture = conditions['texture'])) or None
       q2=(conditions['specification'] and Q(specification = conditions['specification'])) or None
       query_set = filter(lambda x:x!=None,[q1,q2])
       if query_set:
           query_conditions = reduce(lambda x,y:x&y,query_set)
           items_set = OutsideStorageList.objects.filter(query_conditions)
       else:
           items_set = OutsideStorageList.objects.all()
   items_set = items_set.order_by('specification')
   context = {
            'items_set':items_set,
            "search_form":form,
   }
   html = render_to_string("storage/widgets/outsidestorage_table.html",context)
   return simplejson.dumps({"html":html})

@dajaxice_register
def weldMaterialStorageItems(request,specification):
    item_set = WeldStoreList.objects.filter(specification = specification,count__gt = 0).order_by('entry_time')
    html = render_to_string("storage/weldapply/itemlist.html",{"item_set":item_set})
    return simplejson.dumps({'html':html})

@dajaxice_register
def weldMaterialApply(request,apply_form,select_item,aid):
    storageitem = WeldStoreList.objects.get(id = select_item)
    applycard = WeldingMaterialApplyCard.objects.get(id=aid)
    form = WeldApplyKeeperForm(deserialize_form(apply_form),instance=applycard)
    if form.is_valid():
        if applycard.status == APPLYCARD_KEEPER:
            if storageitem.inventory_count >= form.cleaned_data["actual_weight"]:
                applycard.storelist = storageitem
                applycard.save()
                applycard.material_code = storageitem.entry_item.material_code
                form.save()
                message = u"领用单材料选择成功"
                flag = True
            else:
                message = u"领用确认失败，所选库存材料数量不足"
                flag = False
        else:
            flag = False
            message = u"领用卡已经确认，不能修改材料"
    html = render_to_string("storage/wordhtml/weldapply.html",{"apply_card":applycard})   
    return simplejson.dumps({'message':message,'flag':flag,"html":html})

@dajaxice_register
def weldRefundCommit(request,rid,form):
    ref_obj = WeldRefund.objects.get(id = rid)
    reform = WeldRefundForm(deserialize_form(form),instance = ref_obj)
    if reform.is_valid():
        reform.save()
        storageitem = ref_obj.receipts_code.storelist
        storageitem.count += ref_obj.refund_count
        storageitem.save()
        
        ref_obj.weldrefund_status = STORAGESTATUS_END
        ref_obj.save()
        message = u"退库成功，信息已记录"
    else:
        message = u"退库失败，退库单信息未填写完整"
        print reform.errors
        
    is_show = ref_obj.weldrefund_status == STORAGESTATUS_END
    print is_show
    return simplejson.dumps({"is_show":is_show,"message":message})

@dajaxice_register
def changeStorageDb(request,db_type,form):
    db_model = checkStorage(db_type)
    context = {}
    context["check_db_form"] = CheckMaterielDbForm(deserialize_form(form))
    context["check_materiel_form"] = CheckMaterielListForm(db_type = db_model)
    context["items_set"] = db_model.objects.all()
    context["is_production"] = True
    form_html = render_to_string("storage/widgets/checkstorage_search.html",context)
    table_html = render_to_string("storage/widgets/materiel_table.html",context)
    return simplejson.dumps({'form_html':form_html,"table_html":table_html})

@dajaxice_register
def chooseStorageMateriel(request,form,selected):
    form = CheckMaterielListForm(deserialize_form(form))
    if form.is_valid():
        db_type = form.cleaned_data["db_type"]
        db_model = checkStorage(db_type)
    try:
        choosedmateriel = db_model.objects.get(id = selected)
    except Exception,e:
        print e
"""
@dajaxice_register
def searchMateriel(request,form):
    context = getSearchMaterielContext(request,form)
    html = render_to_string("storage/widgets/materiel_table.html",context)
    return simplejson.dumps({"html":html})

def getSearchMaterielContext(request,form,is_production = True):
    db_form = CheckMaterielDbForm(deserialize_form(form))
    if db_form.is_valid():
        db_type = db_form.cleaned_data["db_type"]
        db_model = checkStorage(db_type)
    materiel_form = CheckMaterielListForm(deserialize_form(form),db_type = db_model)
    context = {}
    if materiel_form.is_valid():
        id = materiel_form.cleaned_data["materiel_type"]
        try:
            item = db_model.objects.filter(id = id)
            context["items_set"] = item
        except Exception,e:
            print e
    else:
        print materiel_form.errors
    context["is_production"] = is_production
    return context
"""
@dajaxice_register
def searchWeldEntry(request,searchform):
    form = WeldEntrySearchForm(deserialize_form(searchform))
    if form.is_valid():
        entry_set = get_set_filter(WeldMaterialEntry,form.cleaned_data,replace_dic).order_by("-create_time")
    else:
        print form.errors
        entry_set = []
    print entry_set 
    html = render_to_string("storage/widgets/storageentryhomemain.html",{"entry_set":entry_set,"ENTRYSTATUS_END":STORAGESTATUS_END,"entryurl":"storage/weldentryconfirm"})
    return simplejson.dumps({"html":html})

@dajaxice_register
def searchMaterial(request,search_form,search_type,table_path):
    (storelist_model,form_type,applycard_model) = checkStorage(search_type)
    search_form = form_type(deserialize_form(search_form))
    if search_form.is_valid():
        if search_type=="weld":
            replace_dic = gen_replace_dic(search_form.cleaned_data,"entry_item")
            store_items = get_weld_filter(storelist_model,search_form.cleaned_data,replace_dic).filter(item_status = ITEM_STATUS_NORMAL).order_by("create_time")
        else:
            store_items = get_weld_filter(storelist_model,search_form.cleaned_data)
    html = render_to_string(table_path,{"store_items":store_items,})
    return simplejson.dumps({"html":html})

@dajaxice_register
def weldApplyConfirm(request,role,aid):
    apply_card = WeldingMaterialApplyCard.objects.get(id=aid)
    if role == "keeper":
        if apply_card.storelist != None:
            if apply_card.status == APPLYCARD_KEEPER:
                apply_card.status = APPLYCARD_END
                apply_card.keeper = request.user
                apply_card.save()
                storageitem = apply_card.storelist
                storageitem.inventory_count -= apply_card.actual_weight
                storageitem.save()
                message = u"领用卡确认成功"
            else:
                message = u"领用确认失败，不能重复确认"
        else:
            message = u"领用卡确认失败，请先选择领用的材料"
    html = render_to_string("storage/wordhtml/weldapply.html",{"apply_card":apply_card})  
    return simplejson.dumps({"html":html,"message":message})

@dajaxice_register
def searchWeldRefund(request,search_form):
    search_form = RefundSearchForm(deserialize_form(search_form))
    if search_form.is_valid():
        refund_set = get_weld_filter(WeldRefund,search_form.cleaned_data)
        html = render_to_string("storage/widgets/weldrefundhistorytable.html",{"refund_set":refund_set})
    return simplejson.dumps({"html":html})

@dajaxice_register
def refundKeeperModify(request,form,rid):
    ref_obj = WeldRefund.objects.get(id = rid)
    form = WeldRefundConfirmForm(deserialize_form(form),instance = ref_obj)
    if form.is_valid():
        form.save()
        flag = True
        message = u"信息修改成功"
    else:
        flag = False
        message = u"信息修改失败"

    html = render_to_string("storage/wordhtml/weldrefundconfirm.html",{"ref_obj":ref_obj})
    return simplejson.dumps({"html":html,"message":message,"flag":flag})

@dajaxice_register
def weldRefundConfirm(request,rid,role):
    ref_obj = WeldRefund.objects.get(id = rid)
    if role == "keeper" and ref_obj.weldrefund_status == STORAGESTATUS_KEEPER :
        ref_obj.weldrefund_status = STORAGESTATUS_END
        ref_obj.keeper = request.user
        ref_obj.save()
        storelist_obj = ref_obj.apply_card.storelist
        storelist_obj.inventory_count += ref_obj.refund_weight
        storelist_obj.save()
        message = u"退库单确认成功"
    else:
        message = u"退库单确认失败"

    html = render_to_string("storage/wordhtml/weldrefundconfirm.html",{"ref_obj":ref_obj})
    return simplejson.dumps({"html":html,"message":message})

@dajaxice_register
def steelMaterialApply(request,select_item,mid):
    flag = False
    try:
        storelist = SteelMaterialStoreList.objects.get(id=select_item)
        applyitem = SteelMaterialApplyCardItems.objects.get(id=mid)
        applyitem.storelist = storelist
        if applyitem.apply_card.status == APPLYCARD_KEEPER:
            if applyitem.apply_count <= storelist.count:
                applyitem.save()
                flag = True
                message = u"材料选择成功"
            else:
                message = u"所选材料数量不足"
        else:
            message = u"领用单已经确认不能再修改"
    except Exception,e:
        message = u"材料选择失败"
        print e
        
    return simplejson.dumps({"message":message,"flag":flag})

@dajaxice_register
@transaction.commit_manually
def steelApplyCardConfirm(request,aid,role):
    applycard = SteelMaterialApplyCard.objects.get(id = aid)
    items = applycard.steelmaterialapplycarditems_set.all()
    flag = True
    if role == "keeper" and applycard.status == APPLYCARD_KEEPER:
        applycard.status = APPLYCARD_END
        applycard.keeper = request.user
        applycard.save()
        for item in items:
            storelist = item.storelist
            if storelist != None:
                storelist.count -= item.apply_count
                storelist.save()
            else:
                flag = False
                break;
        if flag:
            message = u"领用单确认成功"
        else:
            applycard.keeper = None
            message = u"还有领用项未分配库存材料"
    else:
        flag = False
        message = u"领用单确认失败"
    html = render_to_string("storage/wordhtml/steelapplycard.html",{"items":items,"applycard":applycard})
    if flag:
        transaction.commit()
    else:
        transaction.rollback()
    return simplejson.dumps({"message":message,"html":html})
