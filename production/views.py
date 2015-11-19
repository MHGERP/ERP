# coding: UTF-8
from django.shortcuts import render
from production.forms import *

def taskAllocationViews(request):
    context={
        "taskallocationform":TaskAllocationSearchForm()
    }

    return render(request,"production/task_allocation.html",context)

def synthesizeFileListViews(request):
    orderIndexForm = OrderIndexForm();
    context={"orderIndexForm":orderIndexForm}
    return render(request,"production/synthesize_filelist.html",context)

def man_hour_summarizeViews(request):
    orderIndexForm = OrderIndexForm();
    context={"orderIndexForm":orderIndexForm}
    return render(request,"production/man_hour_summarize.html",context)
