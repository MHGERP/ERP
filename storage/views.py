# coding:UTF-8

from django.shortcuts import render

from const import *
from const.forms import InventoryTypeForm
from const.utils import *
from django.http import HttpResponseRedirect
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
def weldMaterialHomeViews(request):

    context = {
    
    }
    return render(request,"storage/weldmaterial/weldmaterialhome.html",context)

def weldEntryHomeViews(request):
    weldentry_set = PurchasingEntry.objects.filter(entry_status = ENTRYSTATUS_KEEPER)
    if request.method == "POST":
        search_form = EntrySearchForm(request.POST)
        if search_form.is_valid():
            date = search_form.cleaned_data["date"]
            purchaser = search_form.cleaned_data["purchaser"]
            work_order = search_form.cleaned_data["work_order"]
            qset = get_filter(date,purchaser,work_order)
            if qset:
                qset = reduce(lambda x,y:x&y ,qset)
                print qset
                weldentry_set = PurchasingEntry.objects.filter(qset)
            else:
                weldentry_set = PurchasingEntry.objects.all()
        else:
            print search_form.errors
    else:
        search_form = EntrySearchForm()
    context = {
        "entry_set":weldentry_set,
        "ENTRYSTATUS_END":ENTRYSTATUS_END,
        "search_form":search_form,
    }
    return render(request,"storage/weldmaterial/weldentryhome.html",context)

def weldEntryConfirmViews(request,eid):
    entry = PurchasingEntry.objects.get(id = eid)
    items = PurchasingEntryItems.objects.filter(purchasingentry = entry)
    entry_form = EntryForm(instance = entry)
    entryitem_form = EntryItemsForm()
    is_show = entry.entry_status == ENTRYSTATUS_KEEPER
    if request.method == "POST":
        entry_form = EntryForm(request.POST,instance = entry)
        if entry_form.is_valid():
            entry_form.save()
            entry.keeper = request.user
            entry.entry_status = ENTRYSTATUS_END
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
    context['unhandled_weld_apply_cards']=weld_apply_cards
    context['search_form']=ApplyCardHistorySearchForm()
    return render(request,'storage/weldapply/weldapplycardlist.html',context)

def Weld_Apply_Card_Detail(request):
    context={}
    card_index=int(request.GET['index'])
    apply_card=WeldingMaterialApplyCard.objects.get(index=card_index)
    context['apply_card']=apply_card
    return render(request,'storage/weldapply/weldapplycarddetail.html',context)

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
