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

def weldMaterialHomeViews(request):

    context = {
    
    }
    return render(request,"storage/weldmaterial/weldmaterialhome.html",context)

def weldEntryHomeViews(request):
    weldentry_set = getEntrySet(PurchasingEntry,ENTRYSTATUS_KEEPER)

    context = {
        "entry_set":weldentry_set,    
    }
    return render(request,"storage/weldmaterial/weldentryhome.html",context)

def weldEntryConfirmViews(request,eid):
    entry = PurchasingEntry.objects.get(id = eid)
    items = PurchasingEntryItems.objects.filter(purchasingentry = entry)
    entry_form = EntryForm(instance = entry)
    entryitem_form = EntryItemsForm()

    context = {
        "pur_entry":entry,
        "entry_set":items,
        "entry_form":entry_form,
        "item_form":entryitem_form,
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
