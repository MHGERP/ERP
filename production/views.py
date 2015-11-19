# coding: UTF-8
from django.shortcuts import render
from production.forms import *

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
