# coding: UTF-8
from django.shortcuts import render

def taskAllocationViews(request):
    context={}
    return render(request,"production/task_allocation.html",context)
