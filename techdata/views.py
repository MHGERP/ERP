# coding: UTF-8
from django.shortcuts import render, redirect
from const.forms import InventoryTypeForm
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
import json
from django.db import transaction
from django.contrib.auth.models import User
from backend.utility import getContext


def techPreparationPlanViews(request):
    context = {}
    return render(request, "techdata/tech_preparation_plan.html", context)

def techFileDirectoryViews(request):
    context = {}
    return render(request, "techdata/tech_file_directory.html", context)

def techInstallWeldViews(request):
    context = {}
    return render(request, "techdata/tech_install_weld.html", context)

def techHotDeelViews(request):
    context = {}
    return render(request, "techdata/tech_hot_deel.html", context)
