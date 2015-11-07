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
def weldMaterialHomeViews(request):

    context = {
    
    }
    return render(request,"storage/weldmaterial/weldmaterialhome.html",context)

def weldEntryHomeViews(request):
    weldentry_set = getEntrySet(PurchasingEntry,"keeper")

    context = {
        "entry_set":weldentry_set,    
    }
    return render(request,"storage/weldmaterial/weldentryhome.html",context)

def weldEntryConfirmViews(request,eid):
    entry = PurchasingEntry.objects.get(id = eid)
    items = PurchasingEntryItems.objects.filter(purchasingentry = entry)
    entry_form = EntryForm(instance = entry)

    context = {
        "pur_entry":entry,
        "entry_set":items,
        "entry_form":entry_form,
    }
    return render(request,"storage/weldmaterial/weldentryconfirm.html",context)
