# coding: UTF-8
import datetime
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
from storage.utils import *
from django.shortcuts import render

@dajaxice_register
def get_apply_card_detail(request,apply_card_index):
    context={}
    return render(request,'storage/weldapply/weldapplycarddetail.html',context)

@dajaxice_register
def searchApplyCard(request,form):
    """
    author: Rosen
    summary:process the search request for steel apply card and return the result
    params: search form
    return: search result and message
    """
    form = SteelRefundSearchForm(deserialize_form(form))
    context={}
    if form.is_valid():
        conditions = form.cleaned_data
        steel_apply_cards = get_weld_filter(CommonSteelMaterialApplyCardInfo,conditions)
        print steel_apply_cards
        result_table = render_to_string("storage/widgets/apply_card_table.html",{"apply_cards":steel_apply_cards})
        message = "success"
        context["result_table"]=result_table
    else:
        message = "errors"
    context["message"]=message
    return simplejson.dumps(context)

@dajaxice_register
def searchRefundCard(request,form):
    """
    author: Rosen
    summary:process the search request for steel refund card and return the result
    params: search form
    return: search result and message
    """
    form = SteelRefundSearchForm(deserialize_form(form))
    context={}
    if form.is_valid():
        conditions = form.cleaned_data
        steel_refund_cards = get_weld_filter(CommonSteelMaterialReturnCardInfo,conditions)
        print steel_refund_cards
        result_table = render_to_string("storage/widgets/refund_card_table.html",{"refund_cards":steel_refund_cards})
        message = "success"
        context["result_table"]=result_table
    else:
        message = "errors"
    context["message"]=message
    return simplejson.dumps(context)

@dajaxice_register
def searchSteelLedger(request,form):
    """
    author: Rosen
    summary:process the search request for steel ledger and return the result
    params: search form
    return: search result and message
    """
    form = SteelLedgerSearchForm(deserialize_form(form))
    context={}
    if form.is_valid():
        conditions = form.cleaned_data
        steel_set = get_weld_filter(SteelMaterial,conditions)
        print steel_set
        result_table = render_to_string("storage/widgets/steel_ledger_table.html",{"steel_set":steel_set})
        message = "success"
        context["result_table"]=result_table
    else:
        message = "errors"
    context["message"]=message
    return simplejson.dumps(context)

@dajaxice_register
def Search_History_Apply_Records(request,data):
    context={}
    context['APPLYCARD_COMMIT']=APPLYCARD_COMMIT
    form=ApplyCardHistorySearchForm(deserialize_form(data))
    if form.is_valid():
        conditions=form.cleaned_data
        q1=(conditions['date'] and Q(create_time=conditions['date'])) or None
        q2=(conditions['department'].strip(' ') and Q(department=conditions['department'])) or None
        q3=(conditions['index'] and Q(index=int(conditions['index']))) or None
        q4=(conditions['work_order'] and Q(workorder__order_index=int(conditions['work_order']))) or None
        q5=(conditions['commit_user'] and Q(commit_user__username=conditions['commit_user'])) or None
        qset = filter(lambda x:x!=None,[q1,q2,q3,q4,q5]) 
        if qset:
            query_conditions=reduce(lambda x,y:x&y,qset)
            context['weld_apply_cards'] = WeldingMaterialApplyCard.objects.filter(query_conditions)
        else:
            context['weld_apply_cards']=WeldingMaterialApplyCard.objects.all()
        return render_to_string('storage/weldapply/history_table.html',context)
    else:
        return HttpResponse('FAIL')

@dajaxice_register
def Auxiliary_Detail_Query(request,id):
    context={}
    object_id=int(id)
    auxiliary_tool=AuxiliaryTool.objects.get(id=object_id)
    context['model']=dict(AUXILIARY_TOOLS_MODELS_CHOICES)[int(auxiliary_tool.model)]
    context['measurement_unit']=auxiliary_tool.measurement_unit
    context['unit_price']=auxiliary_tool.unit_price
    return HttpResponse(simplejson.dumps(context))



@dajaxice_register
def Search_Auxiliary_Tools_Records(request,data,search_type):
    context={}
    form=AuxiliaryToolsSearchForm(deserialize_form(data))
    if form.is_valid():
        if search_type=='inventory':
            conditions=form.cleaned_data
            context['rets'] = get_weld_filter(AuxiliaryTool,conditions)
            return render_to_string('storage/auxiliarytools/inventory_table.html',context)
        else:
            conditions=form.cleaned_data
            if search_type=='entry':
                q1=(conditions['date'] and Q(create_time=conditions['date'])) or None
                q2=(conditions['name'] and Q(auxiliary_tool__name=conditions['name'])) or None
                q3=(conditions['model'] and Q(auxiliary_tool__model=conditions['model'])) or None
                q4=(conditions['manufacturer'] and Q(auxiliary_tool__manufacturer=conditions['manufacturer'])) or None
                query_conditions=reduce(lambda x,y:x&y,filter(lambda x:x!=None,[q1,q2,q3,q4]))
                entry_records=AuxiliaryToolEntryCard.objects.filter(query_conditions)
                context['rets']=entry_records
                return render_to_string('storage/auxiliarytools/entry_table.html',context)
            elif search_type=='apply':
                q1=(conditions['date'] and Q(commit_time=conditions['date'])) or None
                q2=(conditions['name'] and Q(actual_item__name=conditions['name'])) or None
                q3=(conditions['model'] and Q(actual_item__model=conditions['model'])) or None
                q4=(conditions['manufacturer'] and Q(actual_item__manufacturer=conditions['manufacturer'])) or None
                query_conditions=reduce(lambda x,y:x&y,filter(lambda x:x!=None,[q1,q2,q3,q4]))                
                apply_records=AuxiliaryToolApplyCard.objects.filter(query_conditions)
                context['rets']=apply_records
                return render_to_string('storage/auxiliarytools/apply_table.html',context)

@dajaxice_register
def Search_Auxiliary_Tools_Apply_Card(request,data):
    context={}
    form=AuxiliaryToolsApplyCardSearchForm(deserialize_form(data))
    if form.is_valid():
        conditions=form.cleaned_data
        q1=(conditions['create_time'] and Q(create_time=conditions['create_time'])) or None
        q2=(conditions['apply_item'] and Q(apply_item__name=conditions['apply_item'])) or None
        q3=(conditions['applicant'] and Q(applicant=conditions['applicant'])) or None
        q4=(conditions['index'] and Q(index=conditions['index'])) or None
        q5=Q(status=1)
        query_conditions=reduce(lambda x,y:x&y,filter(lambda x:x!=None,[q1,q2,q3,q4,q5]))                
        apply_records=AuxiliaryToolApplyCard.objects.filter(query_conditions)
        context['rets']=apply_records
        return render_to_string('storage/auxiliarytools/entry_apply_detail_table.html',context)    

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

    
@dajaxice_register
def entryItemSave(request,form,mid):
    item = WeldMaterialEntryItems.objects.get(id = mid)
    entry_form = EntryItemsForm(deserialize_form(form),instance = item) 
    pur_entry = item.entry
    if entry_form.is_valid():
        entry_form.save()
        flag = True
        message = u"修改成功"
    else:
        print entry_form.errors
        flag = False
        message = u"修改失败"
    entry_set = WeldMaterialEntryItems.objects.filter(entry = pur_entry) 
    html = render_to_string("storage/widgets/weldentrytable.html",{"entry_set":entry_set})
    data = {
        "flag":flag,
        "message":message,
        "html":html,  
    }
    return simplejson.dumps(data)
def steelEntryItemSave(request,form,mid):
    item = SteelMaterialPurchasingEntry.objects.get(id = mid)
    entry_form = SteelEntryItemsForm(deserialize_form(form),instance = item) 
    pur_entry = item.entry
    if entry_form.is_valid():
        entry_form.save()
        flag = True
        message = u"修改成功"
    else:
        print entry_form.errors
        flag = False
        message = u"修改失败"
    entry_set = SteelMaterialPurchasingEntry.objects.filter(entry = pur_entry) 
    html = render_to_string("storage/steelmaterial/steelentryconfirm.html",{"entry_set":entry_set})
    data = {
        "flag":flag,
        "message":message,
        "html":html,  
    }
    return simplejson.dumps(data)

@dajaxice_register
def entryConfirm(request,eid,entry_code):
    try:
        entry = WeldMaterialEntry.objects.get(id = eid)
        if entry.entry_status == STORAGESTATUS_KEEPER:
            entry.entry_code = entry_code
            entry.keeper = request.user
            entry.entry_status = STORAGESTATUS_END
            weldStoreItemsCreate(entry) 
            entry.save()
            flag = True
        else:
            flag = False
    except Exception,e:
        flag = False
        print e
    return simplejson.dumps({'flag':flag})

@dajaxice_register
def getOverTimeItems(request):
    items_set = WeldStoreList.objects.filter(deadline__lt = datetime.date.today() )
    html = render_to_string("storage/widgets/item_table.html",{"items_set":items_set})
    return simplejson.dumps({"html":html})

@dajaxice_register
def getThreadItems(request):
    items_set = WeldStoreList.objects.values("specification").annotate(Sum('count'))
    warning_set = []
    for tmp in items_set:
        try:
            thread = WeldStoreThread.objects.get(specification = tmp["specification"])
            if tmp["count__sum"] < thread.count:
                tmp["count"] = tmp["count__sum"]
                warning_set.append(tmp)
        except Exception,e:
            print e
    html = render_to_string("storage/widgets/item_table.html",{"items_set":warning_set})
    return simplejson.dumps({"html":html})
