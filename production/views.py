# coding: UTF-8
from django.shortcuts import render
from production.forms import *
from const.forms import WorkOrderForm

def taskAllocationViews(request):
    context={
        "taskallocationform":TaskAllocationSearchForm()
    }

    return render(request,"production/task_allocation.html",context)

def taskConfirmViews(request):
    context={
        "taskallocationform":TaskAllocationSearchForm()
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
    context={"productionPlanSearchForm":ProductionPlanSearchForm()}
    return render(request,"production/production_plan.html",context)

def ledgerViews(request):
    context={"ledgerSearchForm":LedgerSearchForm()}
    return render(request,"production/ledger.html",context)
