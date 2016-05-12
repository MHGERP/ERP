#!/usr/bin/env python
# coding=utf-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.utils import simplejson

from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import simplejson
from const import *
from backend.utility import getContext
from sell.forms import *
from sell.models import *

@dajaxice_register
def getProductionList(request, type):
   productions = Product.objects.exclude(is_approval = 0)
   context = {
       "productions" : productions,
   }
   if type == "down":
       return render_to_string("sell/widgets/productions_table.html", context)
   else:
       return render_to_string("sell/widgets/productions_audit_table.html", context)

@dajaxice_register
def getProductionForm(request, iid):
    form = ProductForm()
    context = {
        "form" : form,
    }
    return render_to_string("sell/widgets/production_form.html", context)

@dajaxice_register
def saveProduct(request, form):
    form = ProductForm(deserialize_form(form))
    form.save()
    return "ok"

@dajaxice_register
def getBidFile_issuance(request, param):
    if param == "bidFile_to_manufacture":
        productions = Product.objects.filter(manufacture_file_down__isnull = False)
        path = "sell/widgets/bidFile_to_manufacture_table.html"
    elif param == "bidFile_to_techdata":
        productions = Product.objects.filter(techdata_file_down__isnull = False)
        path = "sell/widgets/bidFile_to_techdata_table.html"
    else:
        productions = Product.objects.filter(purchasing_file_down__isnull = False)
        path = "sell/widgets/bidFile_to_purchasing_table.html"
    context = {
        "productions" : productions,
    }
    return render_to_string(path, context)

@dajaxice_register
def getBidFileForm(request, group, pid):
    product = Product.objects.get(id = pid)
    if group == "manufacture":
        bid = product.manufacture_file_up.id
    elif group == "techdata":
        bid = product.techdata_file_up.id
    else:
        bid = product.purchasing_file_up.id
    form = BidFileAuditForm()
    context = {
        "form" : form,
    }
    html = render_to_string("sell/widgets/bidFileAuditForm.html", context)
    return simplejson.dumps({"html" : html, "bid" : bid})

@dajaxice_register
def saveBidFileStatus(request, bid, sta):
    bidfile = BidFile.objects.get(id = bid)
    bidfile.is_approval = sta
    bidfile.save()
    return "ok"

@dajaxice_register
def saveProductStatus(request, pid):
    product = Product.objects.get(id = pid)
    if product.manufacture_file_up and product.manufacture_file_up.is_approval == 0 and product.techdata_file_up and product.techdata_file_up.is_approval == 0 and product.purchasing_file_up and product.purchasing_file_up.is_approval == 0:
        product.is_approval = 1
        return "ok"
    else:
        return "err"
