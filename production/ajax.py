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
from techdata.models import Processing, CirculationRoute
from django.db import connection
from django.db.models import Q,Sum
from storage.utils import get_weld_filter
from const.forms import WorkOrderForm
from production.forms import *

def getQ(con):
    query_set = Q()
    for k,v in con.items():
         if v:
             query_set.add(Q(**{k: v}), Q.AND)
    return query_set

@dajaxice_register
def getFileList(request, id_work_order):
    """
    Lei
    """
    workorder = SynthesizeFileListStatus.objects.filter(order_id__id = id_work_order)
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
def getHourSearch(request, form):
    """
    Lei
    """
    hour_message_search_form = HourMessageSearchForm(deserialize_form(form))
    if hour_message_search_form.is_valid():
        process_detail_list  = ProcessDetail.objects.filter(getQ(hour_message_search_form.cleaned_data))
    else:
        print hour_message_search_form.errors
    context = {
            "process_detail_list":process_detail_list
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
            process = ProcessDetail.objects.filter(Q(materiel_belong__order__order_index=work_order)&Q(operator__username=operator)&Q(operate_date__year=year)&Q(operate_date__month=month))
        else:
            process = ProcessDetail.objects.filter(Q(materiel_belong__order__order_index=work_order)&Q(operate_date__year=year)&Q(operate_date__month=month))
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
        prodplan_set  = ProductionPlan.objects.filter(getQ(search_form.cleaned_data))
        html = render_to_string("production/widgets/production_plan_table.html",{"prodplan_set":prodplan_set})
    else:
        print search_form.errors
    data = {
        "html":html,
    }
    return simplejson.dumps(data)

@dajaxice_register
def taskAllocationSearch(request, form):
    form = TaskAllocationForm(deserialize_form(form))
    items_list1 = {}
    items_list2 = {}
    if form.is_valid():
        conditions = form.cleaned_data
        q1 = (conditions['workorder']!="-1" and Q(materiel_belong__order=conditions['workorder'])) or None
        q2 = (conditions['identifier'] and Q(materiel_belong__index=conditions['identifier'])) or None
        q3 = (conditions['processnumber'] and Q(name=conditions['processnumber'])) or None
        q4 = None
        from django.contrib.auth.models import User
        from users.models import UserInfo
        if conditions['groupnumber']:
            group = UserInfo.objects.get(name = conditions['groupnumber'])
            q4 = (conditions['groupnumber'] and Q(operator = group.user)) or None
        """q4 = (conditions['groupnumber'] and Q(operator__userinfo__name=conditions['groupnumber'])) or None"""
        query_set = filter(lambda x:x!=None,[q1,q2,q3,q4])
        query = q1 or q2 or q3 or q4
        if query == None:
            items_set1 = Processing.objects.filter(operate_date = None).filter(operator = None)
            items_set2 = Processing.objects.filter(operate_date = None).exclude(operator = None)
        else:
            if query_set :
                query_conditions=reduce(lambda x,y:x&y,query_set)
                items_set1 = Processing.objects.filter(operate_date = None).filter(operator = None).filter(query_conditions)
                items_set2 = Processing.objects.filter(operate_date = None).exclude(operator = None).filter(query_conditions)
            else:
                items_set1 = Processing.objects.filter(operate_date = None).filter(operator = None)
                items_set2 = Processing.objects.filter(operate_date = None).exclude(operator = None)
        for item in items_set2:
            if item.operator != None:
                item.operator.info = item.operator.userinfo

        if conditions['task_allocation_status'] == "-1":
            items_list1 = items_set1
            items_list2 = items_set2
        elif conditions['task_allocation_status'] == "0":
            items_list1 = items_set1
        else:
            items_list2 = items_set2
                    
    user_list = UserInfo.objects.all()
    context = {
        "items_list1":items_list1,
        "items_list2":items_list2,
        "user_list":user_list,
        "taskallocationform":form,
    }
    html = render_to_string("production/table/task_allocation_table.html",context)
    return simplejson.dumps({"html":html})

@dajaxice_register
def taskConfirmSearch(request, form):
    form = TaskConfirmForm(deserialize_form(form))
    items_list1 = {}
    items_list2 = {}
    if form.is_valid():
        conditions = form.cleaned_data
        q1 = (conditions['workorder']!="-1" and Q(materiel_belong__order=conditions['workorder'])) or None
        q2 = (conditions['identifier'] and Q(materiel_belong__index=conditions['identifier'])) or None
        q3 = (conditions['processnumber'] and Q(name=conditions['processnumber'])) or None
        q4 = None
        from django.contrib.auth.models import User
        from users.models import UserInfo
        if conditions['groupnumber']:
            group = UserInfo.objects.get(name = conditions['groupnumber'])
            q4 = (conditions['groupnumber'] and Q(operator = group.user)) or None
        query_set = filter(lambda x:x!=None,[q1,q2,q3,q4])
        query = q1 or q2 or q3 or q4
        if query == None:
            items_set1 = Processing.objects.filter(operate_date = None).exclude(operator = None)
            items_set2 = Processing.objects.exclude(operate_date = None)
        else:
            if query_set:
                query_conditions=reduce(lambda x,y:x&y,query_set)
                items_set1 = Processing.objects.filter(query_conditions).filter(operate_date = None).exclude(operator = None)
                items_set2 = Processing.objects.exclude(operate_date = None).filter(query_conditions)
            else:
                items_set1 = Processing.objects.filter(operate_date =  None).exclude(operator = None)
                items_set2 = Processing.objects.exclude(operate_date = None)
        for item in items_set1:
            if item.operator != None:
                item.operator.info = item.operator.userinfo
        for item in items_set2:
            if item.operator != None:
                item.operator.info = item.operator.userinfo
        if conditions['task_confirm_status'] == "-1":
            items_list1 = items_set1
            items_list2 = items_set2
        elif conditions['task_confirm_status'] == "0":
            items_list1 = items_set1
        else:
            items_list2 = items_set2
    
    user_list = UserInfo.objects.all()
    context = {
        "items_list1":items_list1,
        "items_list2":items_list2,
        "user_list":user_list,
        "taskallocationform":form,
    }
    html = render_to_string("production/table/task_confirm_table.html",context)
    return simplejson.dumps({"html":html})

@dajaxice_register
def taskAllocationRemove(request, form, mid):
   item = Processing.objects.get(id = mid)
   item.operator = None
   item.save()
   return taskAllocationSearch(request, form)
   
@dajaxice_register
def taskAllocationSubmit(request, form, mid, groupid):
    item = Processing.objects.get(id = mid)
    from django.contrib.auth.models import User
    user = User.objects.get(id = groupid)
    item.operator = user
    item.save()
    return taskAllocationSearch(request, form)
      
@dajaxice_register
def taskConfirmFinish(request, form, mid):
    item = Processing.objects.get(id = mid)
    import datetime
    item.operate_date = datetime.datetime.today();
    print datetime.datetime.today()
    item.save()
    return taskConfirmSearch(request, form)


@dajaxice_register
def ledgerSearch(request, form):
    search_form = LedgerSearchForm(deserialize_form(form))
    if search_form.is_valid():
        materiel_list  = Materiel.objects.filter(getQ(search_form.cleaned_data))
        for item in materiel_list:
            if CirculationRoute.objects.filter(materiel_belong = item).count() == 0:
                CirculationRoute(materiel_belong = item).save()
            item.route = '.'.join(getattr(item.circulationroute, "L%d" % i).get_name_display() for i in xrange(1, 11) if getattr(item.circulationroute, "L%d" % i))
        html = render_to_string("techdata/widgets/designBOM_table_list.html",{"BOM":materiel_list})
    else:
        print search_form.errors
    return simplejson.dumps({ "html" : html})

@dajaxice_register
def weldPartOrderInfo(request, iid):
    """
    Lei
    """
    materielObj = Materiel.objects.get(id = iid)
    if CirculationRoute.objects.filter(materiel_belong = materielObj).count() == 0:
        CirculationRoute(materiel_belong = materielObj).save()
    materielObj.route = '.'.join(getattr(materielObj.circulationroute, "L%d" % i).get_name_display() for i in xrange(1, 11) if getattr(materielObj.circulationroute, "L%d" % i))
    materielObj.processDetailObj = ProcessDetail.objects.filter(materiel_belong = materielObj)
    print "ddddd"
    print materielObj.route
    print "ssssss"
    for item in materielObj.processDetailObj:
        print item.process_id

    html = render_to_string("production/widgets/weld_part_order_info_table.html",{"materielObj":materielObj})
    return simplejson.dumps({ "html" : html})
