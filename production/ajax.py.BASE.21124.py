#!/usr/bin/env python
# coding=utf-8

from dajax.core import Dajax
from django.template.loader import render_to_string
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from const.models import WorkOrder,Materiel
from production.models import SynthesizeFileListStatus
from techdata.models import Processing
from django.db import connection
from django.db.models import Q,Sum

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
