# coding:UTF-8
import pprint, pickle
import datetime
from django.shortcuts import render

from const import *
from const.forms import InventoryTypeForm
from const.utils import *
from datetime import datetime
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q,F
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
from django.db import transaction

from storage.models import *
from storage.forms import *
from storage.utils import *
from storage import *
from users import STORAGE_KEEPER

from random import randint

def weldMaterialHomeViews(request):
    hum_set = WeldingMaterialHumitureRecord.objects.all().order_by("-date");
    todayDate = datetime.datetime.now().date()
    if hum_set and hum_set[0].date == todayDate:
        flag = True
    else:
        flag = False
    context = {
            "flag":flag,
            }
    return render(request,"storage/weldmaterial/weldmaterialhome.html",context)

def steelMaterialHomeViews(request):
    context = {

    }
    return render(request,"storage/steelmaterial/steelmaterialhome.html",context)

def steelRefundViews(request):
    search_form = SteelRefundSearchForm()
    refund_cards = SteelMaterialRefundCard.objects.filter(status = REFUNDSTATUS_STEEL_CHOICES_KEEPER)
    context={
            "search_form":search_form,
            "refund_cards":refund_cards,
            "default_status":REFUNDSTATUS_STEEL_CHOICES_KEEPER,
    }
    return render(request,"storage/steelmaterial/steelrefundhome.html",context)

def steelrefunddetailViews(request,rid):
    refund = SteelMaterialRefundCard.objects.get(id=rid)
    if refund.steel_type == BOARD_STEEL:
        items = refund.boardsteelmaterialrefunditems
        html_path = "boardsteelrefunddetail.html"
    else:
        items = refund.barsteelmaterialrefunditems_set.all()
        html_path = "barsteelrefunddetail.html"
    context={
        'refund':refund,
        'items':items,
    }
    return render(request,"storage/steelmaterial/"+html_path,context)


def steelApplyViews(request):
    search_form = SteelApplyCardSearchForm()
    apply_cards = SteelMaterialApplyCard.objects.filter(status = APPLYCARD_KEEPER).order_by("status")
    context={
        "search_form":search_form,
        "apply_cards":apply_cards,
        "APPLYCARD_KEEPER":APPLYCARD_KEEPER,
    }
    return render(request,"storage/steelmaterial/steelapplyhome.html",context)

def steelApplyDetailViews(request,aid):
    apply_type = "steel"
    context = getApplyContext(apply_type,aid)
    return render(request,"storage/steelmaterial/steelapplydetail.html",context)

 
def steelAccountHomeViews(request):
    context = {}
    return render(request,"storage/steelmaterial/steelaccount/steelaccounthome.html",context)

def steelEntryAccountViews(request):
    card_type = "steelentry"
    context = getAccountContext(card_type)
    return render(request,"storage/steelmaterial/steelaccount/steelentryhome.html",context)  


def steelApplyAccountViews(request):
    card_type = "steelapply"
    context = getAccountContext(card_type)
    return render(request,"storage/steelmaterial/steelaccount/steelapplyhome.html",context)  

def steelStorageAccountHomeViews(request):
    card_type = "steelstorage"
    context = getAccountContext(card_type)
    context["room_dispatch"] = True
    return render(request,"storage/steelmaterial/steelaccount/steelstoragehome.html",context)  

def weldEntryHomeViews(request):
    weldentry_set = WeldMaterialEntry.objects.filter(entry_status = ENTRYSTATUS_CHOICES_KEEPER)
    search_form = WeldEntrySearchForm()
    weldentry_set = weldentry_set.order_by("-entry_status","-create_time","-entry_code")
    context = {
            "entry_set":weldentry_set,
            "ENTRYSTATUS_END":ENTRYSTATUS_CHOICES_END,
            "search_form":search_form,
            "entryurl":"storage/weldentryconfirm",
            }
    return render(request,"storage/weldmaterial/weldentryhome.html",context)

def steelEntryHomeViews(request):
    steelentry_set = SteelMaterialEntry.objects.filter(entry_status = ENTRYSTATUS_CHOICES_KEEPER)
    search_form = SteelEntrySearchForm()
    steelentry_set = steelentry_set.order_by("steel_type","-entry_status","-create_time")
    context = {
        "steel_entry_set":steelentry_set,
        "ENTRYSTATUS_END":ENTRYSTATUS_CHOICES_END,
        "search_form":search_form,
    }
    return render(request,"storage/steelmaterial/steelentryhome.html",context)

def weldEntryConfirmViews(request,eid):
    entry = WeldMaterialEntry.objects.get(id = eid)
    items = WeldMaterialEntryItems.objects.filter(entry = entry)
    entryitem_form = EntryItemsForm()
    is_show = entry.entry_status >= ENTRYSTATUS_CHOICES_KEEPER

    context = {
            "entry":entry,
            "items":items,
            "item_form":entryitem_form,
            "is_show":is_show,
            }
    return render(request,"storage/weldmaterial/weldentryconfirm.html",context)

def steelEntryConfirmViews(request,eid):
    entry = SteelMaterialEntry.objects.get(id = eid)
    items = entry.steelmaterialentryitems_set.all()
    form = steelEntryItemsForm()
    remark_form = steelEntryRemarkForm(instance = entry)
    context = {
            "entry":entry,
            "form":form,
            "remark_form":remark_form,
            "items":items,
            "BAR_STEEL":BAR_STEEL,
            }
    return render(request,"storage/steelmaterial/steelmaterialentryconfirm.html",context)
    
def Weld_Apply_Card_List(request):
    """
    Time1ess
    summary: A list of welding Material apply cards
    params: NULL
    return: NULL
    """
    apply_cards=WeldingMaterialApplyCard.objects.filter(status = APPLYCARD_KEEPER).order_by('-create_time')
    context = {
        'APPLYCARD_KEEPER':APPLYCARD_KEEPER,
        'apply_cards':apply_cards,
        'search_form':ApplyCardHistorySearchForm(),
    }
    return render(request,'storage/weldapply/weldapplycardlist.html',context)

def getApplyContext(apply_type,aid):
    store_model,search_material_form_model,apply_card_model,apply_item_model,apply_item_form_model,search_table_path = getApplyDataDict(apply_type)
    apply_card = apply_card_model.objects.get(id=aid)
    search_material_form = search_material_form_model()
    context = {
        "apply_card":apply_card,
        "search_material_form":search_material_form,
        "search_table_path":search_table_path,
        "apply_type":apply_type,
    }
    if apply_type in ["steel","outside"]:
        context["items"] = apply_item_model.objects.filter(apply_card = apply_card)
    if apply_item_form_model != None:
        context["apply_item_form"] = apply_item_form_model()
    return context

def Weld_Apply_Card_Detail(request):
    """
    Time1ess
    summary: The detail information of the given index
    params: index(GET)
    return: NULL
    """
    aid = int(request.GET['index'])
    apply_type = "weld"
    context = getApplyContext(apply_type,aid)
    return render(request,'storage/weldapply/weldapplycarddetail.html',context)

def Handle_Apply_Card_Form(request):
    """
    Time1ess
    summary: Check current user's authority to call the right function
    params: request object
    return: NULL
    """
    if request.method=='POST':
        if checkAuthority(STORAGE_KEEPER,request.user):
            Apply_Card_Form_Commit(request)
        elif request.user.is_authenticated:
            Apply_Card_Form_Apply(request)

        #print apply_card_form
        return HttpResponseRedirect('/storage/weldapply')
    else:
        return HttpResponseRedirect('/storage/weldapply')

def Apply_Card_Form_Apply(request):
    """
    Time1ess
    summary: Handle welding material apply card form in apply stage
    params: index(POST)
    return: NULL
    """
    ac=WeldingMaterialApplyCard.objects.get(index=int(request.POST['index']))
    apply_card_form=ApplyCardForm(request.POST,instance=ac)
    if apply_card_form.is_valid():
        print 'VALID'
        s=apply_card_form.save()
    else:
        print 'INVALID'
        print apply_card_form.errors

def Apply_Card_Form_Commit(request):
    """
    Tim1ess
    summary: Handle welding material apply card form in commit stage
    params: index(POST)
    return: NULL
    """
    ac=WeldingMaterialApplyCard.objects.get(index=int(request.POST['index']))
    apply_card_form=ApplyCardForm(request.POST,instance=ac)
    if apply_card_form.is_valid():
        print 'VALID'
        s=apply_card_form.save(commit=False)
        s.commit_user=request.user
        s.status=APPLYCARD_COMMIT
        s.save()
        storeConsume(ac) 
    else:
        print 'INVALID'
        print apply_card_form.errors



def weldHumitureHomeViews(request):
    """
    kad
    """
    if request.method == "POST":
        search_form = HumSearchForm(request.POST)
        hum_set = []
        if search_form.is_valid():
            hum_set = get_weld_filter(WeldingMaterialHumitureRecord,search_form.cleaned_data)
        else:
            print search_form.errors
    else:
        hum_set = WeldingMaterialHumitureRecord.objects.all().order_by("-date")
        search_form = HumSearchForm()
    hum_set = hum_set.order_by('-date')
    context = {
            "hum_set":hum_set,
            "search_form":search_form,
            }
    return render(request,"storage/weldhumi/weldhumitureHome.html",context)

def weldhumNewRecord(request):
    """
    kad
    """
    if request.method == "POST":
        form = HumRecordForm(request.POST)
        if form.is_valid():
            humrecord = form.save(commit = False)
            humrecord.storeMan = request.user
            humrecord.save()
            return HttpResponseRedirect("weldhumiture")
        else:
            print form.errors
    else:
        form = HumRecordForm()
    
    pk_file = open("weldDemandData.txt", "rb");
    weldDemandData = pickle.load(pk_file);
    
    context = {
            "weldDemandData": weldDemandData,
            "form":form,
            "changeEnable":False,
            }
    return render(request,"storage/weldhumi/weldhumNewRecord.html",context)

def weldhumDetail(request,eid):
    """
    kad
    """
    hum_detail = WeldingMaterialHumitureRecord.objects.get(id = eid)
    form = HumRecordForm(instance = hum_detail)
    changeEnable = hum_detail.date == get_today()
    
    pk_file = open("weldDemandData.txt", "rb");
    weldDemandData = pickle.load(pk_file);
    
    context = {
            "weldDemandData":weldDemandData,
            "form":form,
            "humRecordDate":hum_detail,
            "changeEnable":changeEnable,
            }
    return render(request,"storage/weldhumi/weldhumDetail.html",context)


def weldDemandData(request):
    """
    kad
    """
    """
    weldDemandData = {
        "demandTemperature":60,
        "demandHumidity":70,
    }
    output = open("weldDemandData.txt", "wb");
    pickle.dump(weldDemandData, output)
    output.close()
    """
    pk_file = open("weldDemandData.txt", "rb");
    weldDemandData = pickle.load(pk_file);
    pprint.pprint(weldDemandData);
    context = {
        "weldDemandData":weldDemandData,
    }
    return render(request, "storage/basedata/weldDemandData.html", context)


def storeRoomManageViews(request):
    """
    kad
    """
    new_room = StoreRoomForm()
    room_set = StoreRoom.objects.all().order_by('-id')
    search_form = StoreRoomSearchForm()
    context = {
        "room_set":room_set,
        "search_form":search_form,
        "new_room":new_room,
    }
    return render(request,"storage/basedata/storeroommanage.html", context)


def weldbakeHomeViews(request):
    """
    kad
    """
    if request.method == "POST":
        search_form = BakeSearchForm(request.POST)
        bake_set = []
        if search_form.is_valid():
            bake_set = get_weld_filter(WeldingMaterialBakeRecord,search_form.cleaned_data)
        else:
            print search_form.errors
    else:
        bake_set = WeldingMaterialBakeRecord.objects.all().order_by("-date")
        search_form = BakeSearchForm()
    context = {
            "bake_set":bake_set,
            "search_form":search_form,
            }
    return render(request,"storage/weldbake/weldbakeHome.html",context)

def weldbakeNewRecord(request):
    """
    kad
    """
    if request.method == "POST":
        form = BakeRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("weldbake")
    else:
        form = BakeRecordForm()
    context = {
            "form":form
            }
    return render(request,"storage/weldbake/weldbakeNewRecord.html",context)

def weldbakeDetail(request):
    """
    kad
    """
    context = getWeldBakeDetailContext(request)
    return render(request,"storage/weldbake/weldbakeDetail.html",context)

def getWeldBakeDetailContext(request):
    context = {}
    request_dic,method = getRequestByMethod(request)
    index = request_dic.get("index",None)
    if index != None: 
        weldbake = WeldingMaterialBakeRecord.objects.get(index = index)
        form = BakeRecordForm(instance = weldbake)
        context["weldbake"] = weldbake
    else:
        form = BakeRecordForm()
    context["is_show"] = True
    context["form"] = form
    return context

def weldapplyrefundHomeViews(request):
    """
    kad
    """
    if request.method == "POST":
        search_form = ApplyRefundSearchForm(request.POST)
        workorder_set = []
        if search_form.is_valid():
            workorder_set = get_weld_filter(SubWorkOrder,search_form.cleaned_data)
    else:
        search_form = ApplyRefundSearchForm()
        workorders = WeldingMaterialApplyCard.objects.values("work_order").distinct()
        workorder_set = []
        for i in workorders:
            workorder_set.append(SubWorkOrder.objects.get(id = i["work_order"]))
        #print workorder_set
    context = {
            "workorder_set":workorder_set,
            "search_form":search_form,
            }
    return render(request,"storage/weldapplyrefund/weldapplyrefundHome.html",context)

def weldapplyrefundDetail(request,index):
    """
    kad
    """
    work_order = SubWorkOrder.objects.get(id = index)
    applyrefund_set = WeldingMaterialApplyCard.objects.filter(work_order = work_order,status = APPLYCARD_END)
    context = {
            "work_order":work_order,
            "applyrefund_set":applyrefund_set,
            "default_status":REFUNDSTATUS_CHOICES_END,
            }
    return render(request,"storage/weldapplyrefund/weldapplyrefundDetail.html",context)


def weldRefundViews(request):
    search_form = RefundSearchForm()
    refund_set = WeldRefund.objects.filter(status = REFUNDSTATUS_CHOICES_KEEPER)
    
    context = {
            "search_form":search_form,
            "refund_set":refund_set,
            "default_status":REFUNDSTATUS_CHOICES_KEEPER,
            }
    return render(request,"storage/weldmaterial/weldrefundhome.html",context )

def weldRefundDetailViews(request,rid):
    ref_obj = WeldRefund.objects.get(id = rid)
    is_show = ref_obj.status == REFUNDSTATUS_CHOICES_KEEPER
    reform = WeldRefundConfirmForm()
    card_type = "weldrefund"
    card_status_form = CardStatusStopForm() 
    context = {
            "refund_form":reform,
            "refund":ref_obj,
            "is_show":is_show,
            "card_type":card_type,
            "card_status_form":card_status_form,
            }
    return render(request,"storage/weldmaterial/weldrefunddetail.html",context) 

def AuxiliaryToolsHomeView(request):
    """
    Time1ess
    summary: the home page of the auxiliary tools functions
    params: NULL
    return: NULL
    """
    context={}
    return render(request,'storage/auxiliarytools/home.html',context)

def AuxiliaryToolsEntryListView(request):
    """
    Time1ess
    summary: show the list of auxiliary tools entry
    params: NULL
    return: NULL
    """
    context={}
    context['entry_list']=AuxiliaryToolEntry.objects.filter(entry_status=ENTRYSTATUS_CHOICES_KEEPER).order_by('create_time')
    context['search_form'] = AuxiliaryEntrySearchForm()
    context['default_status'] = ENTRYSTATUS_CHOICES_KEEPER
    return render(request,'storage/auxiliarytools/auxiliarytoolsentry_list.html',context)


def AuxiliaryToolsEntryView(request):
    """
    Time1ess
    summary: return auxiliary tools entry confirm page
    params: id(GET)
    return: NULL
    """
    context = {}
    object_id = int(request.GET['id'])
    auxiliary_tool_entry = AuxiliaryToolEntry.objects.get(
        id=object_id)
    context['entry'] = auxiliary_tool_entry
    context['items'] = AuxiliaryToolEntryItems.objects.filter(
        entry =auxiliary_tool_entry)
    return render(request,
                  'storage/auxiliarytools/auxiliarytoolsentry.html',
                  context)

def AuxiliaryToolsApplyListView(request):
    """
    Time1ess
    summary: A list of auxiliary tool apply cards
    params: NULL
    return: NULL
    """
    context={}
    apply_cards=AuxiliaryToolApplyCard.objects.filter(status__gte = AUXILIARY_TOOL_APPLY_CARD_KEEPER ).order_by('-create_time')
    context['search_form']=AuxiliaryToolsApplyCardSearchForm()
    context['apply_cards']=apply_cards
    context['default_status'] = AUXILIARY_TOOL_APPLY_CARD_KEEPER
    return render(request,'storage/auxiliarytools/auxiliarytoolsapply_list.html',context)


def AuxiliaryToolsApplyView(request):
    """
    Time1ess
    summary: Render auxiliary tool apply and commit page
    params: index(GET)
    return: NULL
    """
    id=int(request.GET['id']) 
    apply_type =  "auxiliarytool"
    context = getApplyContext(apply_type,id)
    return render(request,'storage/auxiliarytools/auxiliarytoolsapply.html',context)

def AuxiliaryToolsLedgerView(request):
    """
    Time1ess
    summary: The home page of auxiliary tools Ledger
    params: NULL
    return: NULL
    """
    context={}
    return render(request,'storage/auxiliarytools/ledger.html',context)

def AuxiliaryToolsLedgerEntryView(request):
    """
    Time1ess
    summary: The list of auxiliary tool entry ledger
    params: NULL
    return: NULL
    """
    card_type = "auxiliarytoolentry"
    context = getAccountContext(card_type)
    return render(request, 'storage/auxiliarytools/ledger_entry.html', context)

def AuxiliaryToolsLedgerEntryCardView(request):
    """
    Time1ess
    summary: The detail of auxiliary tool entry card
    params: id(GET)
    return: NULL
    """
    context={}
    object_id = int(request.GET['id'])
    auxiliary_tool_card_list = AuxiliaryToolEntryCardList.objects.get(
        id=object_id)
    context['object'] = auxiliary_tool_card_list
    context['sub_objects'] = AuxiliaryToolEntryCard.objects.filter(
        card_list=auxiliary_tool_card_list)
    return render(request,
                  'storage/auxiliarytools/entry_card.html',
                  context)

def AuxiliaryToolsLedgerApplyView(request):
    """
    Time1ess
    summary: The list of auxiliary tool apply ledger
    params: NULL
    return: NULL
    """
    card_type = "auxiliarytoolapply"
    context = getAccountContext(card_type)
    return render(request,'storage/auxiliarytools/ledger_apply.html',context)

def AuxiliaryToolsLedgerApplyCardView(request):
    """
    Time1ess
    summary: The detail of auxiliary tool apply card
    params: NULL
    return: NULL
    """
    context={}
    object_id=int(request.GET['id'])
    auxiliary_tool_apply_card=AuxiliaryToolApplyCard.objects.get(id=object_id)
    context['object']=auxiliary_tool_apply_card
    return render(request,'storage/auxiliarytools/apply_card.html',context)

def AuxiliaryToolsLedgerInventoryView(request):
    """
    Time1ess
    summary: The list of auxiliary tool inventory
    params: NULL
    return: NULL
    """
    card_type = "auxiliarytoolstorage"
    context = getAccountContext(card_type)
    context["account_apply_refund_table"] = "storage/accountsearch/auxiliarytool_account_apply_refund_table.html"
    return render(request,'storage/auxiliarytools/ledger_inventory.html',context)

def AuxiliaryToolsEntryApplyDetailView(request):
    """
    [ABANDONED]
    Time1ess
    """
    pass

def getAccountContext(card_type):
    model_type,form_type,account_table_path = getAccountDataDict(card_type) 
    context = {
            "search_form":form_type(),
            "card_type":card_type,
            "account_table_path":account_table_path,
            }
    return context
def weldAccountHomeViews(request):
    context = {}
    return render(request,"storage/weldmaterial/weldaccount/weldaccounthome.html",context)

def weldEntryAccountViews(request):
    card_type = "weldentry"
    context = getAccountContext(card_type)
    return render(request,"storage/weldmaterial/weldaccount/weldentryhome.html",context)

def weldStorageAccountHomeViews(request):
    card_type = "weldstorage"
    context = getAccountContext(card_type)
    context["account_apply_refund_table"] = "storage/accountsearch/weld_account_apply_refund_table.html"
    context["account_item_form"] = WeldAccountItemForm()
    return render(request,"storage/weldmaterial/weldaccount/weldstoragehome.html",context)

def weldApplyAccountViews(request):
    card_type = "weldapply"
    context = getAccountContext(card_type)
    return render(request,"storage/weldmaterial/weldaccount/weldapplyhome.html",context)


def outsideHomeViews(request):
    context = {

            }
    return render(request,"storage/outside/outsidehome.html",context)

def outsideEntryHomeViews(request):
    
    entry_set = OutsideStandardEntry.objects.filter(entry_status = ENTRYSTATUS_CHOICES_KEEPER)
    search_form = OutsideEntrySearchForm()
    context = {
        "card_set":entry_set,
        "default_status":ENTRYSTATUS_CHOICES_KEEPER,
        "search_form":search_form,
    }
    return render(request,"storage/outside/outsideentryhome.html",context)

def getStorageHomeContext(request,_Model,_SearchForm,default_status,url,key_list,order_field):
    if request.method == "POST":
        search_form = _SearchForm(request.POST)
        if search_form.is_valid():
            obj_set = get_weld_filter(_Model,search_form.cleaned_data)
        else:
            print search_form.errors
    else:
        obj_set = _Model.objects.filter(entry_status=default_status)
        search_form = _SearchForm()
    obj_set = obj_set.order_by(order_field)
    context = {
            key_list[0]:obj_set,
            "search_form":search_form,
            key_list[1]:url,
            key_list[2]:STORAGESTATUS_END,
            }
    return context

def outsideEntryConfirmViews(request,eid):
    entry = OutsideStandardEntry.objects.get(id= eid)
    items = OutsideStandardItems.objects.filter(entry = entry)
    form = OutsideEntryItemForm()
    context = {
        "entry":entry,
        "items":items,
        "form":form,
    }
    return render(request,"storage/outside/entryconfirm.html",context)

def getEntryConfirmContext(request,eid,_Model,_Inform,_Reform,entry_url):
    entry_obj = _Model.objects.get(id = eid)
    inform = _Inform(instance = entry_obj)
    reform = _Reform(instance = entry_obj)
    is_show = entry_obj.entry_status == ENTRYSTATUS_CHOICES_END
    entry_set = OutsideStandardItem.objects.filter(entry = entry_obj)
    context = {
        "inform":inform,
        "reform":reform,
        "entry_obj":entry_obj,
        "entryhomeurl":entry_url,
        "is_show":is_show,
        "entry_set":entry_set,
    }
    return context
def StoreThreadViews(request):
    items_set = WeldStoreThread.objects.all()
    entry_form = ThreadEntryItemsForm()
    if request.method == "POST":
        search_form = ThreadSearchForm(request.POST)
        if search_form.is_valid():
            items_set = get_weld_filter(WeldStoreThread,search_form.cleaned_data)
    else:
        search_form = ThreadSearchForm()
    items_set = items_set.order_by('type','specification')
    context = {
        "items_set":items_set,
        "entry_form":entry_form,
        "search_form":search_form,
    }
    return render(request,"storage/storethread/storethread.html",context)

def outsideApplyCardHomeViews(request):
    applycard_set = OutsideApplyCard.objects.filter(status = APPLYCARD_KEEPER)
    search_form = OutsideApplyCardSearchForm()
    context = {
        "card_set":applycard_set,
        "default_status":APPLYCARD_KEEPER,
        "search_form":search_form,
    }
    return render(request,"storage/outside/applycardhome.html",context)

def outsideApplyCardConfirmViews(request,cid):
    apply_type = "outside"
    context = getApplyContext(apply_type,cid)
    return render(request,"storage/outside/applycardconfirm.html",context)

def getOutsideApplyCardConfirmContext(cid,_Inform,url,default_status):
    applycard = OutsideApplyCard.objects.get(id = cid)
    inform = _Inform(instance = applycard)
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

def outsideAccountHomeViews(request):
    context = {}
    return render(request,"storage/outside/accounthome.html",context)

def outsideStorageAccountViews(request):
    card_type = "outsidestorage"
    context = getAccountContext(card_type)
    return render(request,"storage/outside/account/outsidestorageaccount.html",context)

def outsideEntryAccountHomeViews(request):
    card_type = "outsideentry"
    context = getAccountContext(card_type)
    return render(request,"storage/outside/account/entryhome.html",context)

def outsideApplyCardAccountHomeViews(request):
    card_type = "outsideapply"
    context = getAccountContext(card_type)
    return render(request,"storage/outside/account/applycardhome.html",context)



def outsideRefundHomeViews(request):
    refund_cards = OutsideRefundCard.objects.filter(status = REFUNDSTATUS_CHOICES_KEEPER)
    search_form = OutsideRefundSearchForm()
    context = {
        "card_set":refund_cards,
        "default_status":REFUNDSTATUS_CHOICES_KEEPER,
        "search_form":search_form,
    }
    return render(request,"storage/outside/outsiderefundhome.html", context)

def outsideRefundConfirmViews(request,fid):
    refundcard = OutsideRefundCard.objects.get(id=fid)
    items = OutsideRefundCardItems.objects.filter(refundcard = refundcard)
    context = {
        "refund":refundcard,
        "items":items,
    }
    return render(request,"storage/outside/refundcardconfirm.html", context)

