# coding: UTF-8
import pprint, pickle
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
from storage import *
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
        steel_apply_cards = get_weld_filter(SteelMaterialApplyCard,form.cleaned_data).filter(status__in = STORAGE_STATUS_KEEPER_LIST["apply"])
        result_table = render_to_string("storage/widgets/apply_card_table.html",{"apply_cards":steel_apply_cards,"APPLYCARD_KEEPER":APPLYCARD_KEEPER})
        message = "success"
        context["result_table"]=result_table
    else:
        message = "errors"
    context["message"]=message
    return simplejson.dumps(context)

@dajaxice_register
def searchSteelRefundCard(request,form):
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
        steel_refund_cards = get_weld_filter(SteelMaterialRefundCard,conditions).filter(status__in = STORAGE_STATUS_KEEPER_LIST["steelrefund"])
        result_table = render_to_string("storage/widgets/refund_card_table.html",{"refund_cards":steel_refund_cards,"default_status":REFUNDSTATUS_STEEL_CHOICES_KEEPER})
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
    """
    kad
    """
    try:
        entry = AuxiliaryToolEntry.objects.get(id = eid);
        if role == "keeper":
            if entry.entry_status == ENTRYSTATUS_CHOICES_KEEPER:
                entry.keeper = request.user;
                entry.entry_status = ENTRYSTATUS_CHOICES_END;
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
    html = render_to_string("storage/wordhtml/auxiliaryToolEntry.html", {"items":items, "entry":entry});
    data = {
        "html":html,
        "message":message,
    }
    return simplejson.dumps(data);


@dajaxice_register
def weldDemandDataUpdate(request, temp, humi):
    """
    kad
    """
    pk_file = open("weldDemandData.txt","rb");
    weldDemandData = pickle.load(pk_file);
    pk_file.close();

    weldDemandData["demandTemperature"] = temp;
    weldDemandData["demandHumidity"] = humi;
    output = open("weldDemandData.txt", "wb");
    pickle.dump(weldDemandData, output);
    output.close();
    data = {
        "message": u"修改成功", 
    }
    return simplejson.dumps(data);



@dajaxice_register
def Search_History_Apply_Records(request,data):
    context={}
    context['APPLYCARD_KEEPER']=APPLYCARD_KEEPER
    form=ApplyCardHistorySearchForm(deserialize_form(data))
    if form.is_valid():
        context['apply_cards']=get_weld_filter(WeldingMaterialApplyCard,form.cleaned_data).filter(status__in = STORAGE_STATUS_KEEPER_LIST["apply"])
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
    save_ins.status=AUXILIARY_TOOL_APPLY_CARD_APPLICANT
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
def Search_Auxiliary_Tools_Apply_Card(request,form):
    apply_cards = []
    form=AuxiliaryToolsApplyCardSearchForm(deserialize_form(form))
    if form.is_valid():
        replace_dic = gen_replace_dic(form.cleaned_data)
        apply_cards = get_weld_filter(AuxiliaryToolApplyCard,form.cleaned_data,replace_dic).filter(status__in = STORAGE_STATUS_KEEPER_LIST["auapply"])
    else:
        print form.errors
    context = {
        "apply_cards":apply_cards,
        "default_status":AUXILIARY_TOOL_APPLY_CARD_KEEPER,
    } 
    html = render_to_string('storage/auxiliarytools/apply_card_table.html',context)
    return simplejson.dumps({"html":html})

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
    if entry.auth_status(ENTRYSTATUS_CHOICES_KEEPER):
        if entry_form.is_valid():
            entry_form.save()
            flag = True
            message = u"修改成功"
        else:
            print entry_form.errors
            message = u"修改失败"
    else:
        message = u"修改失败，入库单已确认过"
    is_show = entry.entry_status == ENTRYSTATUS_CHOICES_KEEPER
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
        if entry.entry_status == ENTRYSTATUS_CHOICES_KEEPER:
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
        if entry.entry_status == ENTRYSTATUS_CHOICES_KEEPER:
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
    if entry.entry_status == ENTRYSTATUS_CHOICES_KEEPER:
        entry.keeper = request.user
        entry.entry_status = ENTRYSTATUS_CHOICES_END
        entry.save()
        weldStoreItemsCreate(entry)
        message = u"入库单确认成功"
    else:
        message = u"入库单已经确认过,不能重复确认"
    is_show = entry.entry_status == ENTRYSTATUS_CHOICES_KEEPER 
    return {"message":message},is_show

@dajaxice_register
def steelEntryConfirm(request,eid,role):
    try:
        print eid
        entry = SteelMaterialEntry.objects.get(id = eid)
        if role == "keeper": 
            if entry.entry_status == ENTRYSTATUS_CHOICES_KEEPER:
                createSteelMaterialStoreList(entry)
                entry.entry_status = ENTRYSTATUS_CHOICES_END
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
def outsideEntryConfirm(request,eid):
    entry = OutsideStandardEntry.objects.get(id=eid)
    items = OutsideStandardItems.objects.filter(entry = entry)
    if entry.entry_status == ENTRYSTATUS_CHOICES_KEEPER:
        queryset = []
        for item in items:
            queryset.append(OutsideStorageList(entry_item=item,count=item.count,outsidebuy_type=entry.outsidebuy_type))
        OutsideStorageList.objects.bulk_create(queryset)
        entry.entry_status = ENTRYSTATUS_CHOICES_END
        entry.keeper = request.user
        entry.save()
        message = u"入库单确认成功"
    else:
        message = u"入库单确认失败"
    html = render_to_string("storage/wordhtml/outsideentry.html",{"entry":entry,"items":items})
    
    return simplejson.dumps({"html":html,"message":message})

"""
def getEntryData(request,eid,form,_Model,_ItemModel,_Inform,_Reform,entryhomeurl,role,status_list,entry_status=ENTRYSTATUS_CHOICES_KEEPER):
    entry_obj = _Model.objects.get(id = eid)
    form = deserialize_form(form)
    inform = _Inform(form,instance=entry_obj)
    reform = _Reform(form,instance=entry_obj)
    form_list = [("inform",inform),("reform",reform)]
    entryobject = EntryObject(status_list,_Model,eid) 
    context = entryobject.save_entry(entry_obj,role,request.user,form_list)
    is_show = entryobject.checkShow(entry_obj,ENTRYSTATUS_CHOICES_KEEPER)
    context["entryhomeurl"] = entryhomeurl
    context["is_show"]=is_show
    context["entry_set"] = _ItemModel.objects.filter(entry=entry_obj)
    return render_to_string("storage/widgets/entryAbody.html",context),entryobject.flag,context
"""

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
def outsideApplyCardConfirm(request,aid):
    apply_card = OutsideApplyCard.objects.get(id = aid)
    items = OutsideApplyCardItems.objects.filter(apply_card = apply_card)
    if apply_card.status == APPLYCARD_KEEPER:
        if items.filter(storelist__isnull = True).count() > 0:
            message = u"还有领用项未分配库存材料"
        else:
            for item in items:
                storelist = item.storelist
                storelist.count -= item.count
                storelist.save()
            apply_card.status = APPLYCARD_END
            apply_card.keeper = request.user
            apply_card.save()
            message = u"领用卡确认成功"
    else:
        message = u"领用卡已经确认过"
    
    context = {
        "apply_card":apply_card,
        "items":items,
    }
    html = render_to_string("storage/wordhtml/outsideapplycard.html",context)
    return simplejson.dumps({"message":message,"html":html})

def getOutsideApplyCardContext(applycard,inform,url,default_status):
    is_show = applycard.entry_status == default_status
    items_set = OutsideApplyCardItems.objects.filter(apply_card = applycard)
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
        items_set.filter(applycard__entry_status = APPLYCARD_END)
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
            if storageitem.count >= form.cleaned_data["actual_weight"]:
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
        entry_set = get_weld_filter(WeldMaterialEntry,form.cleaned_data).filter(entry_status__in = STORAGE_STATUS_KEEPER_LIST["entry"]).order_by("-create_time")
    else:
        print form.errors
        entry_set = []
    html = render_to_string("storage/widgets/storageentryhomemain.html",{"entry_set":entry_set,"ENTRYSTATUS_END":ENTRYSTATUS_CHOICES_END,"entryurl":"storage/weldentryconfirm"})
    return simplejson.dumps({"html":html})

def getSearchMaterialItems(search_form,apply_type,mid):
    table_path = "storage/searchmaterial/store_"+apply_type+"_items_table.html"
    store_model,search_material_form_model,apply_card_model,apply_item_model,apply_item_form_model,search_table_path = getApplyDataDict(apply_type)
    search_form = search_material_form_model(deserialize_form(search_form))
    if search_form.is_valid():
        replace_dic = gen_replace_dic(search_form.cleaned_data)
        store_items = get_weld_filter(store_model,search_form.cleaned_data,replace_dic,is_show_all=False)
        store_items = store_items.order_by("entry_item__entry__create_time")
    select_item = apply_item_model.objects.get(id=mid).storelist
    return store_items,table_path,select_item
@dajaxice_register
def searchMaterial(request,search_form,apply_type,mid):
    store_items,table_path,select_item = getSearchMaterialItems(search_form,apply_type,mid)
    html = render_to_string(table_path,{"store_items":store_items,"select_item":select_item})
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
                storageitem.count -= apply_card.actual_weight
                storageitem.save()
                message = u"领用卡确认成功"
            else:
                message = u"领用确认失败，不能重复确认"
        else:
            message = u"领用卡确认失败，请先选择领用的材料"
    html = render_to_string("storage/wordhtml/weldapplycard.html",{"apply_card":apply_card})  
    return simplejson.dumps({"html":html,"message":message})

@dajaxice_register
def searchWeldRefund(request,search_form):
    search_form = RefundSearchForm(deserialize_form(search_form))
    if search_form.is_valid():
        refund_set = get_weld_filter(WeldRefund,search_form.cleaned_data).filter(status__in = STORAGE_STATUS_KEEPER_LIST["refund"])
        html = render_to_string("storage/widgets/weldrefundhistorytable.html",{"refund_set":refund_set,"default_status":REFUNDSTATUS_CHOICES_KEEPER})
    return simplejson.dumps({"html":html})

@dajaxice_register
def refundKeeperModify(request,form,rid):
    ref_obj = WeldRefund.objects.get(id = rid)
    form = WeldRefundConfirmForm(deserialize_form(form),instance = ref_obj)
    flag = False
    if ref_obj.status == REFUNDSTATUS_CHOICES_KEEPER:
        if form.is_valid():
            form.save()
            flag = True
            message = u"信息修改成功"
        else:
            message = u"信息修改失败"
    else:
        message = u"退库已经确认过，不能再次修改"
    html = render_to_string("storage/wordhtml/weldrefundconfirm.html",{"refund":ref_obj})
    return simplejson.dumps({"html":html,"message":message,"flag":flag})

@dajaxice_register
def weldRefundConfirm(request,rid,role):
    ref_obj = WeldRefund.objects.get(id = rid)
    if role == "keeper" and ref_obj.status == REFUNDSTATUS_CHOICES_KEEPER :
        ref_obj.status = REFUNDSTATUS_CHOICES_END
        ref_obj.keeper = request.user
        ref_obj.save()
        storelist_obj = ref_obj.apply_card.storelist
        storelist_obj.count += ref_obj.refund_weight
        storelist_obj.save()
        message = u"退库单确认成功"
    else:
        message = u"退库单确认失败"

    html = render_to_string("storage/wordhtml/weldrefundconfirm.html",{"refund":ref_obj})
    return simplejson.dumps({"html":html,"message":message})

@dajaxice_register
def steelMaterialApply(request,select_item,mid):
    flag = False
    try:
        storelist = SteelMaterialStoreList.objects.get(id=select_item)
        applyitem = SteelMaterialApplyCardItems.objects.get(id=mid)
        applyitem.storelist = storelist
        applycard = applyitem.apply_card
        items = SteelMaterialApplyCardItems.objects.filter(apply_card=applycard)
        if applyitem.apply_card.status == APPLYCARD_KEEPER:
            if applyitem.count <= storelist.count:
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
    
    html = render_to_string("storage/wordhtml/steelapplycard.html",{"applycard":applycard,"items":items})
    return simplejson.dumps({"message":message,"flag":flag,"html":html})

@dajaxice_register
def steelApplyCardConfirm(request,aid,role):
    apply_card = SteelMaterialApplyCard.objects.get(id = aid)
    items = apply_card.steelmaterialapplycarditems_set.all()
    if role == "keeper" and apply_card.status == APPLYCARD_KEEPER:
        if items.filter(storelist__isnull = True).count() == 0:
            for item in items:
                storelist = item.storelist
                storelist.count -= item.count
                storelist.save()
            apply_card.status = APPLYCARD_END
            apply_card.keeper = request.user
            apply_card.save()
            message = u"领用单确认成功"
        else:
            message = u"还有领用项未分配库存材料"
    else:
        message = u"领用单确认失败,已经确认过"
    html = render_to_string("storage/wordhtml/steelapplycard.html",{"items":items,"apply_card":apply_card})
    return simplejson.dumps({"message":message,"html":html})

@dajaxice_register
def steelRefundConfirm(request,rid):
    try:
        refund = SteelMaterialRefundCard.objects.get(id=rid)
        if refund.steel_type == BOARD_STEEL:
            items = refund.boardsteelmaterialrefunditems
            items_table_path = "steelboardrefund.html"
        else:
            items = refund.barsteelmaterialrefunditems_set.all()
            items_table_path = "steelbarrefund.html"
        updateSteelStoreList(refund,items)
        refund.status = REFUNDSTATUS_STEEL_CHOICES_END
        refund.keeper = request.user
        refund.save()
        message = u"退库成功"
    except Exception,e:
        message = u"退库失败"
        print e
    items_table_path = "storage/wordhtml/" + items_table_path
    html = render_to_string(items_table_path,{"refund":refund,"items":items})
    return simplejson.dumps({"html":html,"message":message})

def updateSteelStoreList(refund,items):
    if refund.steel_type == BOARD_STEEL:
        old_storelist = items.applyitem.storelist
        return_time = old_storelist.return_time + 1
        new_storelist = SteelMaterialStoreList(entry_item=old_storelist.entry_item,specification=items.specification,steel_type=old_storelist.steel_type,count=items.count,return_time=return_time,weight=items.weight,refund=refund.id)
        new_storelist.save() 
    else:
        for item in items:
            old_storelist = item.applyitem.storelist
            return_time = old_storelist.return_time + 1
            new_storelist = SteelMaterialStoreList(entry_item=old_storelist.entry_item, specification=item.specification, steel_type=old_storelist.steel_type, count=item.count, return_time=return_time, weight=item.weight, length=item.length, refund=refund.id)
            new_storelist.save()


@dajaxice_register
def outsideCardSearch(request,role,form):
    OutsideCardDict = {"entry":OutsideStandardEntry,"applycard":OutsideApplyCard,"refund":OutsideRefundCard}
    OutsideSearchFormDict = {"entry":OutsideEntrySearchForm,"applycard":OutsideApplyCardSearchForm,"refund":OutsideRefundSearchForm}
    OutsideKeepperStatusDict = {"entry":ENTRYSTATUS_CHOICES_KEEPER,"applycard":APPLYCARD_KEEPER,"refund":REFUNDSTATUS_CHOICES_KEEPER}
    OutsideCardStatusKeeperList = {"entry":ENTRY_STATUS_KEEPER_LIST,"applycard":APPLYCARD_STATUS_KEEPER_LIST,"refund":REFUND_STATUS_KEEPER_LIST}
    form = OutsideSearchFormDict[role](deserialize_form(form))
    card_model = OutsideCardDict[role]
    html_path = "storage/widgets/outside"+role+"hometable.html"
    if form.is_valid():
        card_set = get_weld_filter(card_model,form.cleaned_data)
        if role == "entry":
            card_set = card_set.filter(entry_status__in = OutsideCardStatusKeeperList[role])
        else:
            card_set = card_set.filter(status__in = OutsideCardStatusKeeperList[role])
    html = render_to_string(html_path,{"card_set":card_set,"default_status":OutsideKeepperStatusDict[role]})
    return simplejson.dumps({"html":html})

@dajaxice_register
def outsideEntryItemSave(request,form,mid):
    item = OutsideStandardItems.objects.get(id=mid)
    form = OutsideEntryItemForm(deserialize_form(form),instance = item)
    flag = False
    if item.entry.entry_status == ENTRYSTATUS_CHOICES_KEEPER:
        if form.is_valid():
            form.save()
            flag = True
            message = u"材料信息保存成功"
        else:
            message = u"材料信息保存失败"
    else:
        message = u"入库单已经确认过，不能再次修改"
        
    html = render_to_string("storage/outside/entryitemform.html",{"form":form})
    return simplejson.dumps({"message":message,"flag":flag,"html":html})

@dajaxice_register
def getOutsideEntryItemFormInfo(request,mid):
    item = OutsideStandardItems.objects.get(id=mid)
    form = OutsideEntryItemForm(instance = item)
    html = render_to_string("storage/outside/entryitemform.html",{"form":form})
    return simplejson.dumps({"html":html})

@dajaxice_register
def outsideMaterialApply(request,select_item,mid):
    applyitem = OutsideApplyCardItems.objects.get(id=mid)
    storelist = OutsideStorageList.objects.get(id=select_item)
    if applyitem.apply_card.status == APPLYCARD_KEEPER:
        if applyitem.count <= storelist.count:
            applyitem.storelist = storelist
            applyitem.save()
            message = u"材料选择成功"
        else:
            message = u"所选材料数量不足"
    else:
        message = u"领用卡已经确认，不能修改材料"
        
    return simplejson.dumps({"message":message})

@dajaxice_register
def outsideRefundCardConfirm(request,role,fid):
    refundcard = OutsideRefundCard.objects.get(id=fid)
    items = refundcard.outsiderefundcarditems_set.all()
    if role == "keeper":
        if refundcard.status == REFUNDSTATUS_CHOICES_KEEPER:
            for item in items:
                storelist = item.applyitem.storelist
                storelist.count += item.count
                storelist.save()
            refundcard.status = REFUNDSTATUS_CHOICES_END
            refundcard.keeper = request.user
            refundcard.save()
            message = u"退库单确认成功"
        else:
            message = u"退库单已经确认过"
    
    context = {
        "refund":refundcard,
        "items":items,
    }
    html = render_to_string("storage/wordhtml/outsiderefund.html",context)
    return simplejson.dumps({"html":html,"message":message})

@dajaxice_register
def auxiliaryToolMaterialApply(request,select_item,aid,form):
    storelist = AuxiliaryToolStoreList.objects.get(id=select_item)
    applycard = AuxiliaryToolApplyCard.objects.get(id=aid)
    form = AuxiliaryToolsApplyItemForm(deserialize_form(form),instance=applycard)
    if applycard.status == AUXILIARY_TOOL_APPLY_CARD_KEEPER:
        if form.is_valid():
            applycard = form.save(commit=False)
            if applycard.actual_count <= storelist.count:
                applycard.actual_storelist = storelist
                applycard.save()
                message = u"材料选择成功"
            else:
                message = u"所选库存材料数量不足"
        else:
            print form.errors
            message = u"材料选择失败"
    else:
        message = u"领用卡已经确认过，不能修改材料"
    form_html = render_to_string("storage/auxiliarytools/auxiliarytoolsapplyform.html",{"apply_form":form})
    card_html = render_to_string("storage/wordhtml/auxiliarytoolapplycard.html",{"applycard":applycard})
    return simplejson.dumps({'message':message,'form_html':form_html,'card_html':card_html})
   
@dajaxice_register
def auToolApplyCardConfirm(request,role,aid):
    apply_card = AuxiliaryToolApplyCard.objects.get(id=aid)
    if role == "keeper":
        if apply_card.status == AUXILIARY_TOOL_APPLY_CARD_KEEPER:
            storelist = apply_card.storelist
            storelist.count -= apply_card.actual_count
            storelist.save()
            apply_card.status = AUXILIARY_TOOL_APPLY_CARD_END
            apply_card.keeper = request.user
            apply_card.save()
            message = u"领用卡确认成功"
        else:
            message = u"领用卡已经确认过"
    
    card_html = render_to_string("storage/wordhtml/auxiliarytoolapplycard.html",{"apply_card":apply_card})
    return simplejson.dumps({"card_html":card_html,"message":message})

@dajaxice_register
def storageAccountSearch(request,card_type,search_form):
    html = getAccountSearchContext(card_type,search_form)
    return simplejson.dumps({"html":html})

def getAccountSearchContext(card_type,search_form):
    model_type,form_type,account_table_path = getAccountDataDict(card_type)
    search_form = form_type(deserialize_form(search_form))
    if search_form.is_valid():
        replace_dic = gen_replace_dic(search_form.cleaned_data)
        if card_type in ["weldapply","auxiliarytoolapply"]:
            order_field = "create_time"
        elif "entry" in card_type:
            order_field = "entry__create_time"
        elif "apply" in card_type:
            order_field = "apply_card__create_time"
        else:
            order_field = "entry_item__entry__create_time"
        items = get_weld_filter(model_type,search_form.cleaned_data,replace_dic)
        items = getStatusEndItems(items,card_type)
        items = items.order_by(order_field)
        if card_type == "steelstorage":
            for item in items:
                if item.steel_type == BOARD_STEEL and item.return_time > 0:
                    refund = SteelMaterialRefundCard(id = item.refund) 
                    item.graph = refund.boardsteelmaterialrefunditems.graph

    html = render_to_string(account_table_path,{"items":items})
    return html

def getStatusEndItems(items,card_type):
    filter_dict = dict()
    if "entry" in card_type:
        filter_dict["entry__entry_status"] = ENTRYSTATUS_CHOICES_END
    elif card_type in ["weldapply","auxiliarytoolapply"]:
        if card_type == "weldapply":
            filter_dict["status"] = APPLYCARD_END
        else:
            filter_dict["status"] =  AUXILIARY_TOOL_APPLY_CARD_END
    elif "apply" in card_type:
        filter_dict["apply_card__status"] = APPLYCARD_END
    
    if not "storage" in card_type:
        items = items.filter(Q(**filter_dict))
    return items

ApplyCardDict = {"weld":WeldingMaterialApplyCard,"auxiliarytool":AuxiliaryToolApplyCard}
@dajaxice_register
def storageAccountItemForm(request,mid,role):
    storeitem,account_item_form = getAccountItemDataDict(role)
    storeitem = storeitem.objects.get(id=mid)
    account_item_form = account_item_form(instance = storeitem)
    form_html = render_to_string("storage/accountsearch/account_item_form.html",{"account_item_form":account_item_form})
    refundcards = []
    applycards = []
    if ApplyCardDict.has_key(role):
        filter_status = APPLYCARD_END if role == "weld" else AUXILIARY_TOOL_APPLY_CARD_END 
        applycards = ApplyCardDict[role].objects.filter(storelist = storeitem,status = filter_status).order_by("create_time")
        if role == "weld":
            for applycard in applycards:
                try:
                    refund = WeldRefund.objects.get(apply_card = applycard,status = REFUNDSTATUS_CHOICES_END)
                    refundcards.append(refund)
                except Exception,e:
                    print e
    table_html = render_to_string("storage/accountsearch/"+role+"_account_apply_refund_table.html",{"applycards":applycards,"refundcards":refundcards})
    return simplejson.dumps({"table_html":table_html,"form_html":form_html})

@dajaxice_register
def storageAccountItemModify(request,account_item_form,mid,search_form,card_type,role):
    storeitem_model,account_item_form_model = getAccountItemDataDict(role)
    storeitem = storeitem_model.objects.get(id=mid)
    account_item_form = account_item_form_model(deserialize_form(account_item_form),instance = storeitem)
    if account_item_form.is_valid():
        account_item_form.save()
        message = u"库存信息修改成功"
    else:
        message = u"库存信息修改失败"
        print account_item_form.errors
    table_html = getAccountSearchContext(card_type,search_form)
    form_html = render_to_string("storage/accountsearch/account_item_form.html",{"account_item_form":account_item_form})
    return simplejson.dumps({"table_html":table_html,"message":message,"form_html":form_html})

@dajaxice_register
def applyItemRefresh(request,mid,apply_type):
    store_model,search_material_form_model,apply_card_model,apply_item_model,apply_item_form_model,search_table_path = getApplyDataDict(apply_type)
    apply_item = apply_item_model.objects.get(id=mid)
    if apply_item_form_model != None:
        apply_item_form = apply_item_form_model(instance = apply_item)
        form_html = render_to_string("storage/searchmaterial/apply_item_form.html",{"apply_item_form":apply_item_form})
    else:
        form_html = ""
    select_item = apply_item.storelist
    show_html = render_to_string("storage/searchmaterial/show_select_item.html",{"select_item":select_item})
    table_html = render_to_string(search_table_path,{"select_item":select_item})
    return simplejson.dumps({"form_html":form_html,"show_html":show_html,"table_html":table_html})

@dajaxice_register
def searchMaterialApply(request,apply_form,select_item,mid,apply_type,search_form):
    store_model,search_material_form_model,apply_card_model,apply_item_model,apply_item_form_model,search_table_path = getApplyDataDict(apply_type)
    apply_item = apply_item_model.objects.get(id=mid)
    storeitem = store_model.objects.get(id=select_item)
    apply_card = apply_item if apply_type in ["weld","auxiliarytool"] else apply_item.apply_card
    keeper_status = AUXILIARY_TOOL_APPLY_CARD_KEEPER if apply_type == "auxiliarytool" else APPLYCARD_KEEPER
    message,form_html = handle_select_item_result(apply_item_form_model,apply_form,apply_item,keeper_status,storeitem,apply_card,apply_type)
    word_html = getWordHtml(apply_type,apply_card)
    show_html = render_to_string("storage/searchmaterial/show_select_item.html",{"select_item":select_item})
    store_items,table_path,select_item = getSearchMaterialItems(search_form,apply_type,mid)
    table_html = render_to_string(table_path,{"select_item":select_item,"store_items":store_items})
    show_select = select_item != None
    return simplejson.dumps({'message':message,"word_html":word_html,"form_html":form_html,"show_html":show_html,"table_html":table_html,"show_select":show_select})

def handle_select_item_result(apply_item_form_model,apply_form,apply_item,keeper_status,storeitem,apply_card,apply_type):
    count_field = {"weld":"actual_weight","auxiliarytool":"actual_count"}
    if apply_item_form_model != None:
        apply_item_form = apply_item_form_model(deserialize_form(apply_form),instance=apply_item)
        if apply_item_form.is_valid():
            apply_count = apply_item_form.cleaned_data[count_field[apply_type]]
            message,flag = handle_save_select_item_process(apply_card,storeitem,apply_item,apply_count,keeper_status)
            if flag: 
                apply_item_form.save()
        else:
            message = u"材料领用失败，确认信息有误"
        form_html = render_to_string("storage/searchmaterial/apply_item_form.html",{"apply_item_form":apply_item_form})
    else:
        form_html = ""
        apply_count = apply_item.count
        message,flag = handle_save_select_item_process(apply_card,storeitem,apply_item,apply_count,keeper_status)
    return message,form_html

def handle_save_select_item_process(apply_card,storeitem,apply_item,apply_count,keeper_status):
    flag = False
    if apply_card.status == keeper_status:
        if storeitem.count >= apply_count:
            apply_item.storelist = storeitem
            apply_item.save()
            message = u"领用单材料选择成功"
            flag = True
        else:
            message = u"领用确认失败，所选库存材料数量不足"
    else:
        message = u"领用卡已经确认，不能修改材料"
    return message,flag

def getWordHtml(apply_type,apply_card):
    wordhtml_path = "storage/wordhtml/"+apply_type+"applycard.html"
    if apply_type=="weld":
        context = {"apply_card":apply_card}
    elif apply_type == "steel":
        context = {"apply_card":apply_card,"items":apply_card.steelmaterialapplycarditems_set.all()}
    elif apply_type == "outside":
        context = {"apply_card":apply_card,"items":apply_card.outsideapplycarditems_set.all()}
    elif apply_type == "auxiliarytool":
        context = {"apply_card":apply_card}
    word_html = render_to_string(wordhtml_path,context)  
    return word_html

@dajaxice_register
def getAuxiliaryEntrySearch(request,form):
    search_form = AuxiliaryEntrySearchForm(deserialize_form(form))
    if search_form.is_valid():
        replace_dic = gen_replace_dic(search_form.cleaned_data)
        entry_list = get_weld_filter(AuxiliaryToolEntry,search_form.cleaned_data,replace_dic).filter(entry_status__in = STORAGE_STATUS_KEEPER_LIST["entry"]).order_by('create_time')

    context = {
        "entry_list":entry_list,
        'default_status':ENTRYSTATUS_CHOICES_KEEPER,
    }
    html = render_to_string("storage/widgets/auxiliarytoolsentrytable.html",context)
    return simplejson.dumps({"html":html})

@dajaxice_register
def storageSteelRoomDispatchList(request):
    items = SteelMaterialStoreList.objects.filter(store_room__isnull = True)
    html = render_to_string("storage/accountsearch/steelstorage.html",{"items":items})
    return simplejson.dumps({"html":html})

@dajaxice_register
def cardStatusStop(request,stop_card_type,stop_role,form,fid):
    flag = False
    try:
        card_model,div_name,html_path = STORAGE_CARD_DATA_DICT[stop_card_type]
        card_obj = card_model.objects.get(id = fid)
        form = CardStatusStopForm(deserialize_form(form))
        if "entry" in stop_card_type:
            status = card_obj.entry_status
            card_obj.entry_status = STORAGE_CARD_STOP_STATUS
        else:
            status = card_obj.status
            card_obj.status = STORAGE_CARD_STOP_STATUS
        if status == STORAGE_CARD_STOP_STATUS:
            message = u"流程已经终止过不能重复终止"
        else:
            if form.is_valid():
                record = form.save( commit = False )
                record.user = request.user
                record.card_type = stop_card_type
                record.card_id = card_obj.id
                record.save()
                card_obj.save()
                flag = True
                message = u"流程终止成功"
            else:
                message = u"流程终止失败，还没有填写原因"
    except Exception,e:
        print e
        message = u"流程终止失败"

#    if flag:
#        html = render_to_string("storage/wordhtml/"+html_path+".html",{"ref_obj":card_obj})
#    else:
#        html = ""
#        div_name = ""

    form_html = render_to_string("storage/widgets/cardstatusstopform.html",{"card_status_form":form})
    return simplejson.dumps({"message":message,"form_html":form_html})

@dajaxice_register
def steelEntrySearch(request,search_form):
    search_form = SteelEntrySearchForm(deserialize_form(search_form))
    if search_form.is_valid():
        steelentry_set = get_weld_filter(SteelMaterialEntry,search_form.cleaned_data).filter(entry_status__in = STORAGE_STATUS_KEEPER_LIST["entry"])
    else:
        print search_form.errors
        steelentry_set = []
    html = render_to_string("storage/widgets/steelmaterialentrytable.html",{"steel_entry_set":steelentry_set,"ENTRYSTATUS_END":ENTRYSTATUS_CHOICES_END})
    return simplejson.dumps({"html":html})
