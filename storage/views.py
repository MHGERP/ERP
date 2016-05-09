# coding:UTF-8

import datetime
from django.shortcuts import render

from const import *
from const import MATERIAL_TYPE
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
from users import STORAGE_KEEPER

from random import randint

def weldMaterialHomeViews(request):
    context = {

            }
    return render(request,"storage/weldmaterial/weldmaterialhome.html",context)

def steelMaterialHomeViews(request):
    context = {

    }
    return render(request,"storage/steelmaterial/steelmaterialhome.html",context)

def steelRefundViews(request):
    search_form = SteelRefundSearchForm()
    refund_cards = CommonSteelMaterialReturnCardInfo.objects.all()
    context={
            "search_form":search_form,
            "refund_cards":refund_cards,
    }
    return render(request,"storage/steelmaterial/steelrefundhome.html",context)

def steelrefunddetailViews(request,typeid,rid):
    typeid=int(typeid)
    common_Info = CommonSteelMaterialReturnCardInfo.objects.get(id=int(rid))
    if typeid:
        return_cards = common_Info.barsteelmaterialreturncardcontent_set.all()
    else:
        return_cards = common_Info.boardsteelmaterialreturncardcontent_set.all()
    context={
        'return_cards':return_cards,
        'common_Info':common_Info,
    }
    if typeid==1:
        return render(request,"storage/steelmaterial/barsteelrefunddetail.html",context)
    else:
        return render(request,"storage/steelmaterial/boardsteelrefunddetail.html",context)


def steelApplyViews(request):
    search_form = SteelRefundSearchForm()
    apply_cards = CommonSteelMaterialApplyCardInfo.objects.all().order_by("apply_confirm")
    context={
        "search_form":search_form,
        "apply_cards":apply_cards,
    }
    return render(request,"storage/steelmaterial/steelapplyhome.html",context)

def steelApplyDetailViews(request,typeid,rid):
    typeid = int(typeid)
    common_Info = CommonSteelMaterialApplyCardInfo.objects.get(id=int(rid))
    if typeid:
        apply_cards = common_Info.barsteelmaterialapplycardcontent_set.all()
    else:
        apply_cards = common_Info.boardsteelmaterialapplycardcontent_set.all()
    context={
        'apply_cards':apply_cards,
        'common_Info':common_Info,
    }
    if typeid==1:
        return render(request,"storage/steelmaterial/barsteelapplydetail.html",context)
    else:
        return render(request,"storage/steelmaterial/boardsteelapplydetail.html",context)

def steelLedgerViews(request):
    search_form = SteelLedgerSearchForm()
    steel_set = SteelMaterial.objects.all().order_by("steel_type")
    context={
        "search_form":search_form,
        "steel_set":steel_set,
    }
    return render(request,"storage/steelmaterial/steelledger.html",context)
    
def weldEntryHomeViews(request):
    weldentry_set = WeldMaterialEntry.objects.all()
    search_form = WeldEntrySearchForm()
    weldentry_set = weldentry_set.order_by("-entry_status","-create_time","-entry_code")
    context = {
            "entry_set":weldentry_set,
            "ENTRYSTATUS_END":STORAGESTATUS_END,
            "search_form":search_form,
            "entryurl":"storage/weldentryconfirm",
            }
    return render(request,"storage/weldmaterial/weldentryhome.html",context)

def steelEntryHomeViews(request):
    if request.method == "POST":
        search_form = SteelEntrySearchForm(request.POST)
        if search_form.is_valid():
            steelentry_set = get_weld_filter(SteelMaterialEntry,search_form.cleaned_data)
        else:
            print search_form.errors
    else:
        steelentry_set = SteelMaterialEntry.objects.filter(entry_status = STORAGESTATUS_KEEPER)
        search_form = SteelEntrySearchForm()
    steelentry_set = steelentry_set.order_by("steel_type","-entry_status","-create_time")
    context = {
        "steel_entry_set":steelentry_set,
        "ENTRYSTATUS_END":STORAGESTATUS_END,
        "search_form":search_form,
    }
    return render(request,"storage/steelmaterial/steelentryhome.html",context)

def weldEntryConfirmViews(request,eid):
    entry = WeldMaterialEntry.objects.get(id = eid)
    items = WeldMaterialEntryItems.objects.filter(entry = entry)
    entryitem_form = EntryItemsForm()
    is_show = entry.entry_status == STORAGESTATUS_KEEPER
    redict_path = getUrlByViewMode(request,"/storage/weldentryhome")

    context = {
            "entry":entry,
            "items":items,
            "item_form":entryitem_form,
            "is_show":is_show,
            "redict_path":redict_path,
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
    apply_cards=WeldingMaterialApplyCard.objects.all().order_by('-create_time')
    context = {
        'APPLYCARD_KEEPER':APPLYCARD_KEEPER,
        'apply_cards':apply_cards,
        'search_form':ApplyCardHistorySearchForm(),
    }
    return render(request,'storage/weldapply/weldapplycardlist.html',context)

def Weld_Apply_Card_Detail(request):
    """
    Time1ess
    summary: The detail information of the given index
    params: index(GET)
    return: NULL
    """
    card_index=int(request.GET['index'])
    apply_card=WeldingMaterialApplyCard.objects.get(id=card_index)
    apply_form = WeldApplyKeeperForm()
    store_items = WeldStoreList.objects.filter(inventory_count__gt = 0 )
    store_items = modify_weld_item_status(store_items)
    search_material_form = WeldMaterialSearchForm()
    context = {
        "apply_card":apply_card,
        "apply_form":apply_form,
        "APPLYCARD_KEEPER":APPLYCARD_KEEPER,
        "store_items":store_items,
        "ITEM_STATUS_NORMAL":ITEM_STATUS_NORMAL,
        "search_material_form":search_material_form,
    }
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
    context = {
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
    context = {
            "form":form,
            "humRecordDate":hum_detail,
            "changeEnable":changeEnable,
            }
    return render(request,"storage/weldhumi/weldhumDetail.html",context)

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
            workorder_set = get_weld_filter(WorkOrder,search_form.cleaned_data)
    else:
        search_form = ApplyRefundSearchForm()
        workorders = WeldingMaterialApplyCard.objects.values("workorder").distinct()
        workorder_set = []
        for i in workorders:
            workorder_set.append(WorkOrder.objects.get(id = i["workorder"]))
        #print workorder_set
    print search_form
    context = {
            "workorder_set":workorder_set,
            "search_form":search_form,
            }
    return render(request,"storage/weldapplyrefund/weldapplyrefundHome.html",context)

def weldapplyrefundDetail(request,index):
    """
    kad
    """
    workorder = WorkOrder.objects.get(id = index)
    applyrefund_set = WeldingMaterialApplyCard.objects.filter(workorder = workorder)
    context = {
            "workorder":workorder,
            "applyrefund_set":applyrefund_set,
            }
    return render(request,"storage/weldapplyrefund/weldapplyrefundDetail.html",context)


def weldRefundViews(request):
    search_form = RefundSearchForm()
    refund_set = WeldRefund.objects.filter(weldrefund_status = STORAGESTATUS_KEEPER)
    
    context = {
            "search_form":search_form,
            "refund_set":refund_set,
            "STORAGESTATUS_END":STORAGESTATUS_END,
            }
    return render(request,"storage/weldmaterial/weldrefundhome.html",context )

def weldRefundDetailViews(request,rid):
    ref_obj = WeldRefund.objects.get(id = rid)
    is_show = ref_obj.weldrefund_status == STORAGESTATUS_KEEPER
    reform = WeldRefundConfirmForm() 
    context = {
            "refund_form":reform,
            "ref_obj":ref_obj,
            "is_show":is_show,
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
    if request.method=='GET':
        context['entry_list']=AuxiliaryToolEntry.objects.filter(
            entry_status=STORAGESTATUS_KEEPER).order_by('create_time')
    else:
        search_form = AuxiliaryEntrySearchForm(request.POST)
        if search_form.is_valid():
            context['entry_list'] =\
            get_weld_filter(AuxiliaryToolEntry,search_form.cleaned_data).order_by('create_time')
        else:
            context['entry_list']=[]
            print search_form.errors
    context['search_form'] = AuxiliaryEntrySearchForm()
    context['STORAGESTATUS_KEEPER'] = STORAGESTATUS_KEEPER
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
    apply_cards=AuxiliaryToolApplyCard.objects.all().order_by('-create_time')
    context['search_form']=AuxiliaryToolsApplyCardSearchForm()
    context['apply_cards']=apply_cards
    return render(request,'storage/auxiliarytools/auxiliarytoolsapply_list.html',context)


def AuxiliaryToolsApplyView(request):
    """
    Time1ess
    summary: Render auxiliary tool apply and commit page
    params: index(GET)
    return: NULL
    """
    context={}
    ins_index=int(request.GET['index']) 
    ins=AuxiliaryToolApplyCard.objects.get(index=ins_index) if ins_index!=0 else None

    if checkAuthority(STORAGE_KEEPER,request.user):
        context['instance']=ins
        context['storage_keeper']=True
        context['apply_form']=AuxiliaryToolsCardCommitForm(instance=ins)
    else:
        context['storage_keeper']=False
        context['apply_form']=AuxiliaryToolsCardApplyForm()

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
    context = {}
    if request.method == 'GET':
        context['rets'] = AuxiliaryToolEntryCardList.objects.filter(
            status=STORAGESTATUS_END).order_by('-create_time')
    else:
        search_form = AuxiliaryEntrySearchForm(request.POST)
        if search_form.is_valid():
            context['rets'] = get_weld_filter(AuxiliaryToolEntryCardList,
                                              search_form.cleaned_data)\
                    .filter(status=STORAGESTATUS_END)
        else:
            context['rets'] = []
            print search_form.errors
    context['search_form'] = AuxiliaryEntrySearchForm()
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
    context={}
    context['search_form']=AuxiliaryToolsSearchForm()
    context['rets']=AuxiliaryToolApplyCard.objects.filter(status=AUXILIARY_TOOL_APPLY_CARD_COMMITED)
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
    context={}
    context['search_form']=AuxiliaryToolsSearchForm()
    context['rets']=AuxiliaryTool.objects.all()
    return render(request,'storage/auxiliarytools/ledger_inventory.html',context)

def AuxiliaryToolsEntryApplyDetailView(request):
    """
    [ABANDONED]
    Time1ess
    """
    pass

def weldAccountHomeViews(request):
    context = {}
    return render(request,"storage/weldmaterial/weldaccount/weldaccounthome.html",context)

def weldEntryAccountViews(request):
    items_set = WeldStoreList.objects.all().order_by("specification","entry_time")
    if request.method == "POST":
        search_form = WeldAccountSearchForm(request.POST)
        if search_form.is_valid():
            items_set = get_weld_filter(WeldStoreList,search_form.cleaned_data)
    else:
        search_form = WeldAccountSearchForm()
        items_set = items_set.order_by("entry_time")
    context = {
            "items_set":items_set,
            "search_form":search_form,
            }
    return render(request,"storage/weldmaterial/weldaccount/weldentryhome.html",context)

def weldStorageAccountHomeViews(request):
    if request.method == "POST":
        search_form = WeldStorageSearchForm(request.POST)
        if search_form.is_valid():
            items_set = get_weld_filter(WeldStoreList,search_form.cleaned_data)
    else:
        items_set = WeldStoreList.objects.qualified_set().order_by('specification')
        search_form = WeldStorageSearchForm()
    items_set = items_set.order_by("entry_time")
    context = {
            "items_set":items_set,
            "search_form":search_form,
            }
    return render(request,"storage/weldmaterial/weldaccount/weldstoragehome.html",context)

def weldApplyAccountViews(request):
    apply_set = WeldingMaterialApplyCard.objects.all()
    if request.method == "POST":
        search_form =  WeldApplyAccountSearchForm(request.POST)
        if search_form.is_valid():
            apply_set = get_weld_filter(WeldingMaterialApplyCard,search_form.cleaned_data)
        else:
            print search_form.errors
    else:
        search_form = WeldApplyAccountSearchForm()
    context = {
        "apply_set":apply_set,
        "search_form":search_form,
    }
    return render(request,"storage/weldmaterial/weldaccount/weldapplyhome.html",context)


def outsideHomeViews(request):
    context = {

            }
    return render(request,"storage/outside/outsidehome.html",context)

def outsideEntryHomeViews(request):
    key_list = ["entry_set","entryurl","ENTRYSTATUS_END"]
    context = getStorageHomeContext(request,OutsideStandardEntry,OutsideEntrySearchForm,STORAGESTATUS_KEEPER,"storage/outside/entryconfirm",key_list,"entry_time")
    context["check_materiel_form"] = CheckMaterielListForm()
    context["is_production"] = True
    context["items_set"] = WeldStoreList.objects.all()
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
    entry_url = getUrlByViewMode(request,"outside/entryhome")
    context = getEntryConfirmContext(request,eid,OutsideStandardEntry,StorageOutsideEntryInfoForm,StorageOutsideEntryRemarkForm,entry_url)
    return render(request,"storage/outside/entryconfirm.html",context)

def getEntryConfirmContext(request,eid,_Model,_Inform,_Reform,entry_url):
    entry_obj = _Model.objects.get(id = eid)
    inform = _Inform(instance = entry_obj)
    reform = _Reform(instance = entry_obj)
    is_show = entry_obj.entry_status == STORAGESTATUS_KEEPER
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
    applyurl = "storage/outside/applycardconfirm"
    key_list = ["card_set","applyurl","APPLYSTATUS_END"]
    context = getStorageHomeContext(request,OutsideApplyCard,OutsideApplyCardSearchForm,STORAGESTATUS_KEEPER,applyurl,key_list,"date")
    return render(request,"storage/outside/applycardhome.html",context)

def outsideApplyCardConfirmViews(request,cid):
    url = getUrlByViewMode(request,"outside/applycardhome")
    default_status = STORAGESTATUS_KEEPER

    context = getOutsideApplyCardConfirmContext(cid,OutsideApplyCardForm,url,default_status) 
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
    items_set = OutsideStorageList.objects.order_by('specification')
    search_form = OutsideStorageSearchForm()
    items_set = items_set.order_by('specification')
    context = {
        "items_set":items_set,
        "search_form":search_form,
    }
    return render(request,"storage/outside/outsidestorageaccount.html",context)
def outsideEntryAccountHomeViews(request):
    search_form = OutsideAccountEntrySearchForm()
    entry_set = OutsideStandardEntry.objects.filter(entry_status = STORAGESTATUS_END)
    items_set = OutsideStandardItem.objects.filter(entry__in = entry_set)
    from operator import attrgetter
    sorted_items_set = sorted(items_set,key=attrgetter('materiel.order.order_index','specification'))
    context = {
        "search_form":search_form,
        "items_set":sorted_items_set,
        "STORAGESTATUS_END":STORAGESTATUS_END,
    }
    
    return render(request,"storage/outside/account/entryhome.html",context)

def outsideApplyCardAccountHomeViews(request):
    search_form = OutsideAccountApplyCardSearchForm()
    card_set = OutsideApplyCard.objects.filter(entry_status = STORAGESTATUS_END)
    items_set = OutsideApplyCardItem.objects.filter(applycard__in = card_set)
    from operator import attrgetter
    sorted_items_set = sorted(items_set,key=attrgetter('applycard.workorder.order_index','specification'))
    context = {
        "search_form":search_form,
        "items_set":sorted_items_set,
    }

    return render(request,"storage/outside/account/applycardhome.html",context)


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
