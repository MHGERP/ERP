# coding: UTF-8
from django.shortcuts import render
from production.forms import *
from const.forms import WorkOrderForm

def taskAllocationViews(request):
    search_form = TaskAllocationForm()
    from django.contrib.auth.models import User
    from users.models import UserInfo
    items_list1 = Processing.objects.filter(operate_date = None).filter(operator = None)
    items_list2 = Processing.objects.filter(operate_date = None).exclude(operator = None)
    for item in items_list2:
        if item.operator != None:
            item.operator.info = item.operator.userinfo

    user_list = UserInfo.objects.all()

    context={
        "taskallocationform":search_form,
        "user_list":user_list, 
        "items_list1":items_list1,
        "items_list2":items_list2,
    }

    return render(request,"production/task_allocation.html",context)

def taskConfirmViews(request):
    search_form = TaskConfirmForm()
    from django.contrib.auth.models import User
    from users.models import UserInfo
    items_list1 = Processing.objects.filter(operate_date = None).exclude(operator = None)
    items_list2 = Processing.objects.exclude(operate_date = None)
    for item in items_list1:
        if item.operator != None:
            item.operator.info = item.operator.userinfo
    for item in items_list2:
        if item.operator != None:
            item.operator.info = item.operator.userinfo
    user_list = UserInfo.objects.all()
    
    context={
        "taskallocationform":search_form,
        "user_list":user_list, 
        "items_list1":items_list1,
        "items_list2":items_list2,
    }
    return render(request,"production/task_confirm.html",context)

def materielUseViews(request):
    context={}
    return render(request,"production/materiel_use.html",context)

def synthesizeFileListViews(request):
    workOrderForm = WorkOrderForm();
    context={
        "workOrderForm":workOrderForm,
    }
    return render(request,"production/synthesize_filelist.html",context)

def man_hour_messageViews(request):
    hourMessageSearchForm = HourMessageSearchForm()
    context={
        "hourMessageSearchForm":hourMessageSearchForm
    }
    return render(request,"production/man_hour_message.html",context)

def man_hour_summarizeViews(request):
    dateForm = DateForm();
    context={
        "dateForm":dateForm
    }
    return render(request,"production/man_hour_summarize.html",context)

def production_planViews(request):
    #prodplan_set = ProductionPlan.objects.all()
    prodplan_form = ProdPlanForm()
    productionplan_search_form = ProductionPlanSearchForm()
    workorder_search_form = WorkOrderProductionSearchForm()
    context = {
        "prodplan_form": prodplan_form,
        "productionplan_search_form" : productionplan_search_form,
        "workorder_search_form" : workorder_search_form,
    }
    return render(request,"production/production_plan.html",context)

def ledgerViews(request):
    context={"ledgerSearchForm":LedgerSearchForm()}
    return render(request,"production/ledger.html",context)
