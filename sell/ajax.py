#!/usr/bin/env python
# coding=utf-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.utils import simplejson

from django.db.models import Q
from django.contrib.auth.models import User

from const import *
from backend.utility import getContext
from sell.forms import *

@dajaxice_register
def getProductionList(request):
   productions = Product.objects.all()
   context = {
       "productions" : productions,
   }
   return render_to_string("sell/widgets/productions_table.html", context)

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
