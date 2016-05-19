# coding: UTF-8
from django.shortcuts import render
from production.forms import *
from production.models import *
from const.forms import WorkOrderForm
def taskPlanViews(request):
    search_form = TaskPlanForm()
    items_list = ProcessDetail.objects.filter(productionworkgroup = None).order_by('sub_materiel_belong').order_by('-plan_startdate')

    context={
        "taskplanform":search_form,
        "items_list":items_list,
    }

    return render(request,"production/task_plan.html",context)

def taskAllocationViews(request):
    search_form = TaskAllocationForm()
    items_list = ProcessDetail.objects.exclude(plan_startdate = None).filter(complete_process_date = None).order_by('-productionworkgroup')
    for item in items_list:
        item.groups = ProductionWorkGroup.objects.filter(processname = item.processname)

    context={
        "taskallocationform":search_form,
        "items_list":items_list,
    }

    return render(request,"production/task_allocation.html",context)

def taskConfirmViews(request):
    search_form = TaskConfirmForm()
    items_list = ProcessDetail.objects.exclude(productionworkgroup = None).order_by('complete_process_date')

    context={
        "taskallocationform":search_form,
        "items_list":items_list,
    }
    return render(request,"production/task_confirm.html",context)

def materielUseViews(request):
    context={
        "applyCardForm":ApplyCardForm(),
        "materielCopyForm":MaterielCopyForm()
    }
    return render(request,"production/materiel_use.html",context)

def synthesizeFileListViews(request):
    subWorkOrderForm = SubWorkOrderForm();
    context={
        "subWorkOrderForm":subWorkOrderForm,
    }
    return render(request,"production/synthesize_filelist.html",context)

def man_hour_messageViews(request):
    hourMessageSearchForm = HourMessageSearchForm()
    context={
        "hourMessageSearchForm":hourMessageSearchForm
    }
    return render(request,"production/man_hour_message.html",context)

def man_hour_summarizeViews(request):
    hourSummarizeForm = HourSummarizeForm();
    context={
        "hourSummarizeForm":hourSummarizeForm
    }
    return render(request,"production/man_hour_summarize.html",context)

def production_planViews(request):
    productionplan_search_form = ProductionPlanSearchForm()
    workorder_search_form = WorkOrderProductionSearchForm()
    context = {
        "productionplan_search_form" : productionplan_search_form,
        "workorder_search_form" : workorder_search_form,
    }
    return render(request,"production/production_plan.html",context)

def ledgerViews(request):
    context={"ledgerSearchForm":LedgerSearchForm()}
    return render(request,"production/ledger.html",context)

def production_user_manageViews(request):
    context={
        "productionUserSearchForm":ProductionUserSearchForm(),
        "userChooseForm":UserChooseForm()
    }
    return render(request,"production/production_user_manage.html",context)
