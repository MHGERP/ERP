# coding:UTF-8

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

def steelApplyViews(request):
    search_form = SteelRefundSearchForm()
    apply_cards = CommonSteelMaterialApplyCardInfo.objects.all()
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
    steel_set = SteelMaterial.objects.all()
    context={
        "search_form":search_form,
        "steel_set":steel_set,
    }
    return render(request,"storage/steelmaterial/steelledger.html",context)


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
    
def weldEntryHomeViews(request):
    if request.method == "POST":
        search_form = EntrySearchForm(request.POST)
        weldentry_set = []
        if search_form.is_valid():
            weldentry_set = get_weld_filter(WeldMaterialEntry,search_form.cleaned_data)
        else:
            print search_form.errors
    else:
        #weldentry_set = WeldMaterialEntry.objects.filter(entry_status = STORAGESTATUS_KEEPER)
        weldentry_set = WeldMaterialEntry.objects.all()
        search_form = EntrySearchForm()
    context = {
            "entry_set":weldentry_set,
            "ENTRYSTATUS_END":STORAGESTATUS_END,
            "search_form":search_form,
            }
    return render(request,"storage/weldmaterial/weldentryhome.html",context)

def steelEntryHomeViews(request):
    if request.method == "POST":
        search_form = EntrySearchForm(request.POST)
        steelentry_set = []
        if search_form.is_valid():
            steelentry_set = get_weld_filter(SteelMaterialPurchasingEntry,search_form.cleaned_data)
        else:
            print search_form.errors
    else:
        steelentry_set = SteelMaterialPurchasingEntry.objects.all()
        search_form = EntrySearchForm()
    context = {
        "entry_set":steelentry_set,
        "ENTRYSTATUS_END":STORAGESTATUS_END,
        "search_form":search_form,
    }
    return render(request,"storage/steelmaterial/steelentryhome.html",context)

def weldEntryConfirmViews(request,eid):
    entry = WeldMaterialEntry.objects.get(id = eid)
    items = WeldMaterialEntryItems.objects.filter(entry = entry)
    entryitem_form = EntryItemsForm()
    is_show = entry.entry_status == STORAGESTATUS_KEEPER

    context = {
            "entry":entry,
            "entry_set":items,
            "item_form":entryitem_form,
            "is_show":is_show,
            }
    return render(request,"storage/weldmaterial/weldentryconfirm.html",context)

def steelEntryConfirmViews(request,eid):
    entry = SteelMaterialPurchasingEntry.objects.get(id = eid)
    context = {
                "entry":entry,
    }
    return render(request,"storage/steelmaterial/steelentryconfirm.html",context)
    
def Weld_Apply_Card_List(request):
    """
    Time1ess
    summary: A list of welding Material apply cards
    params: NULL
    return: NULL
    """
    context={}
    context['APPLYCARD_COMMIT']=APPLYCARD_COMMIT
    weld_apply_cards=WeldingMaterialApplyCard.objects.exclude(status=APPLYCARD_COMMIT).order_by('create_time')
    context['weld_apply_cards']=weld_apply_cards
    context['search_form']=ApplyCardHistorySearchForm()
    return render(request,'storage/weldapply/weldapplycardlist.html',context)

def Weld_Apply_Card_Detail(request):
    """
    Time1ess
    summary: The detail information of the given index
    params: index(GET)
    return: NULL
    """
    context={}
    card_index=int(request.GET['index'])
    apply_card=WeldingMaterialApplyCard.objects.get(index=card_index)
    context['apply_card']=apply_card 
    context['APPLYCARD_COMMIT']=APPLYCARD_COMMIT
    if request.user.is_superuser:#如果是库管员
        context['apply_card_form']=Commit_ApplyCardForm(instance=apply_card)
    else:#如果是申请者
        context['apply_card_form']=Apply_ApplyCardForm(instance=apply_card)
    return render(request,'storage/weldapply/weldapplycarddetail.html',context)

def Handle_Apply_Card_Form(request):
    """
    Time1ess
    summary: Check current user's authority to call the right function
    params: request object
    return: NULL
    """
    if request.method=='POST':
        if request.user.is_superuser:
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
            form.save()
            return HttpResponseRedirect("weldhumiture")
    else:
        form = HumRecordForm()
    context = {
            "form":form
            }
    return render(request,"storage/weldhumi/weldhumNewRecord.html",context)

def weldhumDetail(request,eid):
    """
    kad
    """
    print eid
    hum_detail = WeldingMaterialHumitureRecord.objects.get(id = eid)
    form = HumRecordForm(instance = hum_detail)
    context = {
            "form":form,
            "humRecordDate":hum_detail,
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

def weldbakeDetail(request,index):
    """
    kad
    """
    bake_detail = WeldingMaterialBakeRecord.objects.get(index = index)
    form = BakeRecordForm(instance = bake_detail)
    context = {
            "form":form,
            }
    return render(request,"storage/weldbake/weldbakeDetail.html",context)

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
    #for i in apply_set:
    #    print i.weldrefund.department
    context = {
            "workorder":workorder,
            "applyrefund_set":applyrefund_set,
            }
    return render(request,"storage/weldapplyrefund/weldapplyrefundDetail.html",context)


def weldRefundViews(request):
    getUserByAuthority(STORAGE_KEEPER)
    if request.method == "POST":
        search_form = RefundSearchForm(request.POST)
        if search_form.is_valid():
            refund_set = get_weld_filter(WeldRefund,search_form.cleaned_data)
    else:
        search_form = RefundSearchForm()
        #refund_set = WeldRefund.objects.filter(weldrefund_status = STORAGESTATUS_KEEPER)
        refund_set = WeldRefund.objects.all()
    context = {
            "search_form":search_form,
            "refund_set":refund_set,
            "STORAGESTATUS_END":STORAGESTATUS_END,
            }
    return render(request,"storage/weldmaterial/weldrefundhome.html",context )

def weldRefundDetailViews(request,rid):
    ref_obj = WeldRefund.objects.get(id = rid)
    is_show = ref_obj.weldrefund_status == STORAGESTATUS_KEEPER
    if request.method == "POST":
        reform = WeldRefundForm(request.POST,instance = ref_obj)
        if reform.is_valid():
            reform.save()
            ref_obj.keeper = request.user
            ref_obj.weldrefund_status = STORAGESTATUS_END
            ref_obj.save()
            return HttpResponseRedirect("/storage/weldrefund")
        else:
            print reform.errors
    else:
        reform = WeldRefundForm(instance = ref_obj) 
    context = {
            "reform":reform,
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
    context['auxiliarytools']=AuxiliaryTool.objects.all()
    return render(request,'storage/auxiliarytools/auxiliarytoolsentry_list.html',context)

def AuxiliaryToolsEntryView(request):
    """
    Time1ess
    summary: Auxiliary tools entry
    params: id(GET,POST),quantity(POST)
    return: NULL
    """
    context={}
    if request.method=='POST':
        object_id=int(request.POST['object_id'])
        auxiliarytool=AuxiliaryTool.objects.get(id=object_id)
        new_entry_quantity=float(request.POST['quantity'])
        if new_entry_quantity<0:
            return HttpResponseRedirect('/storage/auxiliarytools/entrylist')
        auxiliarytool.quantity=F('quantity')+new_entry_quantity
        auxiliarytool.save()
        entryrecord=AuxiliaryToolEntryCard(auxiliary_tool=auxiliarytool,quantity=new_entry_quantity)
        entryrecord.save()
        return AuxiliaryToolsEntryListView(request)
    else:
        object_id=int(request.GET['id'])
        auxiliarytool=AuxiliaryTool.objects.get(id=object_id)
        context['object_id']=object_id
        context['entry_form']=AuxiliaryToolsForm(initial={'quantity':0},instance=auxiliarytool)
        return render(request,'storage/auxiliarytools/auxiliarytoolsentry.html',context)

def AuxiliaryToolsApplyListView(request):
    """
    Time1ess
    summary: A list of auxiliary tool apply cards
    params: NULL
    return: NULL
    """
    context={}
    apply_cards=AuxiliaryToolApplyCard.objects.exclude(status=AUXILIARY_TOOL_APPLY_CARD_COMMITED).order_by('-create_time')
    context['search_form']=AuxiliaryToolsApplyCardSearchForm()
    context['apply_cards']=apply_cards
    return render(request,'storage/auxiliarytools/auxiliarytoolsapply_list.html',context)


def AuxiliaryToolsApplyView(request):
    """
    Time1ess
    summary: Handle auxiliary tool apply
    params: index(GET,POST)
    return: NULL
    """
    context={}
    if request.method=='GET':
        ins_index=int(request.GET['index']) 
        ins=AuxiliaryToolApplyCard.objects.get(index=ins_index) if ins_index!=0 else None

        if request.user.is_superuser:
            context['instance']=ins
            context['apply_form']=AuxiliaryToolsCardCommitForm(instance=ins)
        else:
            context['apply_form']=AuxiliaryToolsCardApplyForm()

        #apply or commit setting
        return render(request,'storage/auxiliarytools/auxiliarytoolsapply.html',context)
    else:
        ins_index=int(request.POST['index'])
        if ins_index!=0:
            ins=AuxiliaryToolApplyCard.objects.get(index=ins_index)
        else:
            ins=None

        apply_card=AuxiliaryToolsCardCommitForm(request.POST,instance=ins)
        if apply_card.is_valid():
            apply_card.save()
        else:
            print apply_card.errors
        return AuxiliaryToolsApplyListView(request)

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
    context={}
    context['search_form']=AuxiliaryToolsSearchForm()
    context['rets']=AuxiliaryToolEntryCard.objects.all()
    return render(request,'storage/auxiliarytools/ledger_entry.html',context)

def AuxiliaryToolsLedgerEntryCardView(request):
    """
    Time1ess
    summary: The detail of auxiliary tool entry card
    params: id(GET)
    return: NULL
    """
    context={}
    object_id=int(request.GET['id'])
    auxiliary_tool_entry_card=AuxiliaryToolEntryCard.objects.get(id=object_id)
    context['object']=auxiliary_tool_entry_card
    return render(request,'storage/auxiliarytools/entry_card.html',context)

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
    context = {
            "items_set":items_set,
            "search_form":search_form,
            }
    return render(request,"storage/weldmaterial/weldaccount/weldentryhome.html",context)

def weldStorageAccountHomeViews(request):
    items_set = WeldStoreList.objects.all().order_by('specification').order_by("entry_time")
    if request.method == "POST":
        search_form = WeldStorageSearchForm(request.POST)
        if search_form.is_valid():
            items_set = get_weld_filter(WeldStoreList,search_form.cleaned_data)
    else:
        search_form = WeldStorageSearchForm()
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
            print search_form.cleaned_data
            apply_set = get_weld_filter(WeldingMaterialApplyCard,search_form.cleaned_data)
            print apply_set
        else:
            print search_form.errors
    else:
        search_form = WeldApplyAccountSearchForm()
    context = {
        "apply_set":apply_set,
        "search_form":search_form,
    }
    return render(request,"storage/weldmaterial/weldaccount/weldapplyhome.html",context)
