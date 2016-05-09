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
