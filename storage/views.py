# coding:UTF-8

from django.shortcuts import render

from const import *
from const.forms import InventoryTypeForm
from const.utils import *
from datetime import datetime
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q

from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
from django.db import transaction

from purchasing.models import PurchasingEntry,PurchasingEntryItems
from purchasing.forms import EntryForm 
from storage.models import *
from storage.forms import *
from storage.utils import *
from users import STORAGE_KEEPER
def weldMaterialHomeViews(request):

    context = {
    
    }
    return render(request,"storage/weldmaterial/weldmaterialhome.html",context)

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
        weldentry_set = PurchasingEntry.objects.filter(entry_status = STORAGESTATUS_KEEPER)
        search_form = EntrySearchForm()
    context = {
        "entry_set":weldentry_set,
        "ENTRYSTATUS_END":STORAGESTATUS_END,
        "search_form":search_form,
    }
    return render(request,"storage/weldmaterial/weldentryhome.html",context)

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
    hum_set = WeldingMaterialHumitureRecord.objects.all().order_by("date") 
    context = {
        "hum_set":hum_set,    
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

def weldRefundViews(request):
    getUserByAuthority(STORAGE_KEEPER)
    if request.method == "POST":
        search_form = RefundSearchForm(request.POST)
        print search_form
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
