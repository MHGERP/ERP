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

def man_hour_summarizeViews(request):
    orderIndexForm = OrderIndexForm();
    context={"orderIndexForm":orderIndexForm}
    return render(request,"production/man_hour_summarize.html",context)

def production_planViews(request):
    orderIndexForm = OrderIndexForm();
    context={"orderIndexForm":orderIndexForm}
    return render(request,"production/production_plan.html",context)

def ledgerViews(request):
    orderIndexForm = OrderIndexForm();
    context={"orderIndexForm":orderIndexForm}
    return render(request,"production/ledger.html",context)
