#!/usr/bin/env python
# coding=utf-8

from dajax.core import Dajax
from django.template.loader import render_to_string
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from const.models import WorkOrder,Materiel
from production.models import *
from production.forms import *
from techdata.models import Processing
from django.db import connection
from django.db.models import Q,Sum
from storage.utils import get_weld_filter
from const.forms import WorkOrderForm

@dajaxice_register
def getFileList(request, id_work_order):
    """
    Lei
    """
    workorder = SynthesizeFileListStatus.objects.filter(workorder_id__id = id_work_order)
    context = {
        "workorder":workorder,
    }
    html = render_to_string("production/synthesize_detail_filelist.html",context)
    return html

@dajaxice_register
def changeFileList(request, id, workorder_id):
    """
    Lei
    """
    workorder = SynthesizeFileListStatus.objects.filter(workorder_id__order_index = workorder_id)[0]
    exec("workorder.%s=True"%id)
    workorder.save()
    context = {
        "workorder":[workorder],
    }
    html = render_to_string("production/synthesize_detail_filelist.html",context)
    return html

@dajaxice_register
def getHourSearch(request, id_work_order, work_ticket, group_num):
    """
    Lei
    """
    if work_ticket:
        materiel = Materiel.objects.filter(order__order_index=id_work_order,index=work_ticket)
    else:
        materiel = Materiel.objects.filter(order__order_index=id_work_order)
    processSet = []
    for item in materiel:
        if group_num:
            process = Processing.objects.filter(materiel_belong=item,operator__username=group_num);
            processSet.append(process)
        else:
            process = Processing.objects.filter(materiel_belong=item);
            processSet.append(process)
    context = {
        "processSet":processSet
    }
    html = render_to_string("production/man_hour_message_list.html",context)
    return html

@dajaxice_register
def getHourSummarize(request, work_order, operator, date):
    """
    Lei
    """
    message = ""
    try:
        year,month = date.split("-")
        if operator:
            process = Processing.objects.filter(Q(materiel_belong__order__order_index=work_order)&Q(operator__username=operator)&Q(operate_date__year=year)&Q(operate_date__month=month))
        else:
            process = Processing.objects.filter(Q(materiel_belong__order__order_index=work_order)&Q(operate_date__year=year)&Q(operate_date__month=month))
        status = 1
    except Exception,e:
        status = 0
        message = "日期格式不正确"
    processSet=set()
    process_filter = []
    for item in process:
        if item.operator not in processSet:
            processSet.add(item.operator)
            process_filter.append(item)
    context = {
        "process":process_filter,
        "date":date
    }
    html = render_to_string("production/widgets/man_hour_table.html",context)
    ret = {
        "status":status,
        "message":message,
        "html":html
    }
    return simplejson.dumps(ret)

@dajaxice_register
def getSummarizeTicket(request, work_order, operator, date):
    """
    Lei
    """
    message = ""
    try:
        year,month = date.split("-")
        process = Processing.objects.filter(Q(materiel_belong__order__order_index=work_order)&Q(operator__username=operator)&Q(operate_date__year=year)&Q(operate_date__month=month)).order_by('operate_date')
        summarize = reduce(lambda x,y:x+y.hour,process,0)
        status = 1
    except Exception,e:
        status = 0
        message = "日期格式不正确"
    
    context = {
        "work_order":work_order,
        "summarize":summarize,
        "process":process,
    }
    html = render_to_string("production/man_hour_summarize_table.html",context)
    ret = {
        "status":status,
        "message":message,
        "html":html
    }
    return simplejson.dumps(ret)

@dajaxice_register
def getPartTicket(request, work_order, operator, date):
    """
    Lei
    """
    message = ""
    try:
        year,month = date.split("-")
        process = Processing.objects.filter(Q(materiel_belong__order__order_index=work_order)&Q(operator__username=operator)&Q(operate_date__year=year)&Q(operate_date__month=month)).order_by('materiel_belong')
        status = 1
    except Exception,e:
        status = 0
        message = "日期格式不正确"

    context = {
        "operator":operator,
        "work_order":work_order,
        "process":process
    }
    html = render_to_string("production/man_hour_part_ticket.html",context)
    ret = {
        "status":status,
        "message":message,
        "html":html
    }
    return simplejson.dumps(ret)



@dajaxice_register
def workorderSearch(request, workSearchText):
    """
    kad
    """
    workorder_set = WorkOrder.objects.filter(order_index__startswith=workSearchText)
    html = render_to_string("production/widgets/production_plan_select_table.html",{"workorder_set":workorder_set})
    data = {
        "html":html,
    }
    return simplejson.dumps(data)

@dajaxice_register
def workorderAdd(request, checkList):
    """
    kad
    """
    for i in checkList:
        wo_obj = WorkOrder.objects.get(order_index = i)
        obj = ProductionPlan(workorder_id = wo_obj)
        obj.save()
    prodplan_set = ProductionPlan.objects.all()
    html = render_to_string("production/widgets/production_plan_table.html", {"prodplan_set":prodplan_set})
    data = {
        "html":html,
    }
    return simplejson.dumps(data)

@dajaxice_register
def prodplanDelete(request, planid):
    """
    kad
    """
    try:
        prodplan_obj = ProductionPlan.objects.get(plan_id = planid)
        prodplan_obj.delete()
        flag = True
    except Exception,e:
        print e
        flag = False
    data = {
        "flag":flag,
    }
    return simplejson.dumps(data)

@dajaxice_register
def prodplanUpdate(request, form, planid):
    """
    kad
    """
    prodplan_obj = ProductionPlan.objects.get(plan_id = planid)
    prodplan_form = ProdPlanForm(deserialize_form(form), instance = prodplan_obj)
    if prodplan_form.is_valid():
        prodplan_form.save()
        message = u"修改成功"
        flag = True
    else:
        message = u"修改失败"
        flag = False
    prodplan_set = ProductionPlan.objects.all()
    html = render_to_string("production/widgets/production_plan_table.html", {"prodplan_set":prodplan_set})

    data ={
        "html":html,
        "message":message,
        "flag":flag,
    }
    return simplejson.dumps(data)

@dajaxice_register
def prodplanSearch(request, form):
    """
    kad
    """
    search_form = ProductionPlanSearchForm(deserialize_form(form))
    if search_form.is_valid():
        #prodplan_set = get_weld_filter(ProductionPlan, search_form.cleaned_data, {"work_order": "workorder_id"})
        con = search_form.cleaned_data
        print con

        q1 = (con["work_order"] and Q(workorder_id = con["work_order"])) or None
        #q1 = None
        q2 = (con["status"] and Q(status = con["status"])) or None
        if con["status"]== "-1":
            q2 = None
        year,month = con["plan_date"].split("-")
        q3 = (con["plan_date"] and Q(plan_date__year = year) & Q(plan_date__month = month)) or None
        #q3 = None
        print q3
        query_set = filter(lambda x:x!=None, [q1,q2,q3])
        if query_set:
            query_con = reduce(lambda x,y:x&y, query_set)
            print query_con
            prodplan_set = ProductionPlan.objects.filter(query_con)
        else:
            prodplan_set = ProductionPlan.objects.all()
        html = render_to_string("production/widgets/production_plan_table.html",{"prodplan_set":prodplan_set})
    else:
        print search_form.errors
    data = {
        "html":html,
    }
    return simplejson.dumps(data)
    
