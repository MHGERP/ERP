# coding: UTF-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from const import *
from const.models import Materiel,OrderFormStatus, BidFormStatus
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib.auth.models import User
from django.db import transaction 
from const.models import WorkOrder, Materiel
from const.forms import InventoryTypeForm
from django.http import HttpResponseRedirect
from django.db.models import Q
from datetime import datetime
from storage.models import *
from django.shortcuts import render

@dajaxice_register
def get_apply_card_detail(request,apply_card_index):
    context={}
    print apply_card_index
    return render(request,'storage/weldapply/weldapplycarddetail.html',context)
