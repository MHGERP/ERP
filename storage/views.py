# coding:UTF-8

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
def weldMaterialHomeViews(request):

    context = {
    
    }
    return render(request,"storage/weldmaterial/weldmaterialhome.html",context)

def steelMaterialHomeViews(request):
    context = {

    }
    return render(request,"storage/steelmaterial/steelmaterialhome.html",context)
    
def weldEntryHomeViews(request):
    if request.method == "POST":
        search_form = EntrySearchForm(request.POST)
        weldentry_set = []
        if search_form.is_valid():
            dict = {}
            dict["entry_time"] = search_form.cleaned_data["date"]
            dict["purchaser"] = search_form.cleaned_data["purchaser"]
            dict["work_order"] = search_form.cleaned_data["work_order"]
            weldentry_set = get_weld_filter(PurchasingEntry,dict)
        else:
            print search_form.errors
    else:
        weldentry_set = WeldMaterialEntry.objects.filter(entry_status = STORAGESTATUS_KEEPER)
        search_form = EntrySearchForm()
    context = {
        "entry_set":weldentry_set,
        "ENTRYSTATUS_END":STORAGESTATUS_END,
        "search_form":search_form,
    }
    return render(request,"storage/weldmaterial/weldentryhome.html",context)

def steelEntryHomeViews(request):
    steelentry_set = getEntrySet(PurchasingEntry,ENTRYSTATUS_KEEPER)

    context  = {
        "entry_set":steelentry_set,
    }
    return render(request,"storage/steelmaterial/steelentryhome.html",context)

def weldEntryConfirmViews(request,eid):
    entry = PurchasingEntry.objects.get(id = eid)
    items = PurchasingEntryItems.objects.filter(purchasingentry = entry)
    entry_form = EntryForm(instance = entry)
    entryitem_form = EntryItemsForm()
    is_show = entry.entry_status == STORAGESTATUS_KEEPER
    if request.method == "POST":
        entry_form = EntryForm(request.POST,instance = entry)
        if entry_form.is_valid():
            entry_form.save()
            entry.keeper = request.user
            entry.entry_status = STORAGESTATUS_END
            entry.save()
            return HttpResponseRedirect("/storage/weldentryhome")
        else:
            print entry_form.errors
    else:
        entry_form = EntryForm(instance = entry)
    context = {
        "pur_entry":entry,
        "entry_set":items,
        "entry_form":entry_form,
        "item_form":entryitem_form,
        "is_show":is_show,
    }
    return render(request,"storage/weldmaterial/weldentryconfirm.html",context)

def Weld_Apply_Card_List(request):
    context={}
    weld_apply_cards=WeldingMaterialApplyCard.objects.filter(commit_user=None).order_by('create_time')#考虑效率问题，注意更改all的获取方式
    context['weld_apply_cards']=weld_apply_cards
    context['search_form']=ApplyCardHistorySearchForm()
    return render(request,'storage/weldapply/weldapplycardlist.html',context)

def Weld_Apply_Card_Detail(request):
    context={}
    card_index=int(request.GET['index'])
    apply_card=WeldingMaterialApplyCard.objects.get(index=card_index)
    context['apply_card']=apply_card
    if request.user.is_superuser:#如果是库管员
        context['apply_card_form']=Commit_ApplyCardForm(instance=apply_card)
    else:#如果是申请者
        context['apply_card_form']=Apply_ApplyCardForm(instance=apply_card)
    return render(request,'storage/weldapply/weldapplycarddetail.html',context)

def Handle_Apply_Card_Form(request):
    if request.method=='POST':
        if request.user.is_superuser:
            Apply_Card_Form_Commit(request)
        elif request.user.is_authenticated:
            Apply_Card_Form_Apply(request)

        #print apply_card_form
        return HttpResponse('RECEIVE')
    else:
        return HttpResponse('FAIL')

def Apply_Card_Form_Apply(request):
    ac=WeldingMaterialApplyCard.objects.get(index=int(request.POST['index']))
    apply_card_form=ApplyCardForm(request.POST,instance=ac)
    if apply_card_form.is_valid():
        print 'VALID'
        s=apply_card_form.save()
    else:
        print 'INVALID'
        print apply_card_form.errors

def Apply_Card_Form_Commit(request):
    ac=WeldingMaterialApplyCard.objects.get(index=int(request.POST['index']))
    apply_card_form=ApplyCardForm(request.POST,instance=ac)
    if apply_card_form.is_valid():
        print 'VALID'
        s=apply_card_form.save(commit=False)
        s.commit_user=request.user
        s.status=3
        s.save()
    else:
        print 'INVALID'
        print apply_card_form.errors



def weldHumitureHomeViews(request):
    if request.method == "POST":
        search_form = HumSearchForm(request.POST)
        dict = {}
        hum_set = []
        if search_form.is_valid():
            dict["date"] = search_form.cleaned_data["date"]
            dict["storeRoom"] = search_form.cleaned_data["storeRoom"]
            dict["storeMan"] = search_form.cleaned_data["storeMan"]
            hum_set = get_weld_filter(WeldingMaterialHumitureRecord,dict)
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
    print eid
    hum_detail = WeldingMaterialHumitureRecord.objects.get(id = eid)
    form = HumRecordForm(instance = hum_detail)
    context = {
        "form":form,
        "humRecordDate":hum_detail,
    }
    return render(request,"storage/weldhumi/weldhumDetail.html",context)

def weldbakeHomeViews(request):
    if request.method == "POST":
        search_form = BakeSearchForm(request.POST)
        dict = {}
        bake_set = []
        if search_form.is_valid():
            dict["date"] = search_form.cleaned_data["date"]
            dict["standardnum"] = search_form.cleaned_data["standardnum"]
            dict["weldengineer"] = search_form.cleaned_data["weldengineer"]
            dict["storeMan"] = search_form.cleaned_data["storeMan"]
            bake_set = get_weld_filter(WeldingMaterialBakeRecord,dict)
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
    bake_detail = WeldingMaterialBakeRecord.objects.get(index = index)
    form = BakeRecordForm(instance = bake_detail)
    context = {
        "form":form,
    }
    return render(request,"storage/weldbake/weldbakeDetail.html",context)

def weldRefundViews(request):
    getUserByAuthority(STORAGE_KEEPER)
    if request.method == "POST":
        search_form = RefundSearchForm(request.POST)
        if search_form.is_valid():
            dict = {}
            dict["date"] = search_form.cleaned_data["date"]
            dict["department"] = search_form.cleaned_data["department"]
            dict["code"] = search_form.cleaned_data["refund_code"]
            dict["work_order"] = search_form.cleaned_data["work_order"]
            dict["keeper"] = search_form.cleaned_data["keeper"]
            refund_set = get_weld_filter(WeldRefund,dict)
    else:
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
    if request.method == "POST":
        reform = WeldRefundForm(request.POST,instance = ref_obj)
        if reform.is_valid():
            reform.save()
            ref_obj.keeper = request.user
            ref_obj.save()
            return HttpResponseRedirect("/storage/weldrefund")
    else:
        reform = WeldRefundForm(instance = ref_obj) 
    context = {
        "reform":reform,
        "ref_obj":ref_obj,
        "is_show":is_show,
    }
    return render(request,"storage/weldmaterial/weldrefunddetail.html",context) 

def AuxiliaryToolsHomeView(request):
    context={}
    return render(request,'storage/auxiliarytools/home.html',context)

def AuxiliaryToolsEntryListView(request):
    context={}
    context['auxiliarytools']=AuxiliaryTool.objects.all()
    return render(request,'storage/auxiliarytools/auxiliarytoolsentry_list.html',context)

def AuxiliaryToolsEntryView(request):
    context={}
    if request.method=='POST':
        object_id=int(request.POST['object_id'])
        auxiliarytool=AuxiliaryTool.objects.get(id=object_id)
        new_entry_quantity=float(request.POST['quantity'])
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

def AuxiliaryToolsApplyView(request):
    context={}
    context['apply_form']=AuxiliaryToolsCardForm()
    return render(request,'storage/auxiliarytools/auxiliarytoolsapply.html',context)

def AuxiliaryToolsLedgerView(request):
    context={}
    return render(request,'storage/auxiliarytools/ledger.html',context)

def AuxiliaryToolsLedgerEntryView(request):
    context={}
    context['search_form']=AuxiliaryToolsSearchForm()
    return render(request,'storage/auxiliarytools/ledger_entry.html',context)

def AuxiliaryToolsLedgerEntryCardView(request):
    context={}
    object_id=int(request.GET['id'])
    auxiliary_tool_entry_card=AuxiliaryToolEntryCard.objects.get(id=object_id)
    context['object']=auxiliary_tool_entry_card
    return render(request,'storage/auxiliarytools/entry_card.html',context)

def AuxiliaryToolsLedgerApplyView(request):
    context={}
    context['search_form']=AuxiliaryToolsSearchForm()
    return render(request,'storage/auxiliarytools/ledger_apply.html',context)

def AuxiliaryToolsLedgerApplyCardView(request):
    context={}
    object_id=int(request.GET['id'])
    auxiliary_tool_apply_card=AuxiliaryToolApplyCard.objects.get(id=object_id)
    context['object']=auxiliary_tool_apply_card
    return render(request,'storage/auxiliarytools/apply_card.html',context)

def AuxiliaryToolsLedgerInventoryView(request):
    context={}
    context['search_form']=AuxiliaryToolsSearchForm()
    return render(request,'storage/auxiliarytools/ledger_inventory.html',context)

def AuxiliaryToolsEntryApplyDetailView(request):
    context={}
    return render(request,'storage/auxiliarytools/entry_apply_detail.html',context)
