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

def processExaminationViews(request):
    context = {}
    return render(request, "techdata/process_examinationViews.html", context)

def techFileDirectoryViews(request):
    context = {}
    return render(request, "techdata/tech_file_directory.html", context)

def firstFeedingViews(request):
    context = {}
    return render(request, "techdata/first_feeding.html", context)

def principalMaterialViews(request):
    context = {}
    return render(request, "techdata/principal_material.html", context)

def processBOMViews(request):
    context = {}
    return render(request, "techdata/processBOM.html", context)

def weldListViews(request):
    context = {}
    return render(request, "techdata/weld_list.html", context)

def weldQuotaViews(request):
    context = {}
    return render(request, "techdata/weld_quota.html", context)
def weldEditViews(request):
    context = {}
    return render(request, "techdata/weld_edit.html", context)

def programmeEditViews(request):
    context = {}
    return render(request, "techdata/programme_edit.html", context)

