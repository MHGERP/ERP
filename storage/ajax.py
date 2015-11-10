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
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q
from datetime import datetime
from storage.models import *
from storage.forms import *
from django.shortcuts import render

@dajaxice_register
def get_apply_card_detail(request,apply_card_index):
    context={}
    print apply_card_index
    return render(request,'storage/weldapply/weldapplycarddetail.html',context)

@dajaxice_register
def Search_History_Apply_Records(request,data):
    context={}
    form=ApplyCardHistorySearchForm(deserialize_form(data))
    if form.is_valid():
        conditions=form.cleaned_data
        q1=(conditions['date'] and Q(create_time=conditions['date'])) or None
        q2=(conditions['department'].strip(' ') and Q(department=conditions['department'])) or None
        q3=(conditions['index'] and Q(index=int(conditions['index']))) or None
        q4=(conditions['work_order'] and Q(workorder__order_index=int(conditions['work_order']))) or None
        q5=(conditions['commit_user'] and Q(commit_user__username=conditions['commit_user'])) or None
        query_conditions=reduce(lambda x,y:x&y,filter(lambda x:x!=None,[q1,q2,q3,q4,q5]))
        apply_records=WeldingMaterialApplyCard.objects.filter(query_conditions)
        print query_conditions
        return render_to_string('storage/weldapply/history_table.html',{'weld_apply_cards':apply_records})

    else:
        return HttpResponse('FAIL')

"""
@dajaxice_register
def weldhum_insert(request,hum_params):
    hum_params=deserialize_form(hum_params)
    form = HumRecordForm(hum_params)
    if form.is_valid():
        form.save()
        message = u"录入成功"
        flag = True
    else:
        flag = False
        message = u"录入失败"
     
    html = render_to_string("storage/widgets/humiture_form.html",{"form":form,})
    data = {
        "flag":flag,
        "html":html,
        "message":message,
    }
    return simplejson.dumps(data)
"""

    
