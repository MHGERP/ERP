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

from const.forms import WorkOrderForm

def techPreparationPlanViews(request):
    context = {}
    return render(request, "techdata/tech_preparation_plan.html", context)

def processExaminationViews(request):
    context = {}
    return render(request, "techdata/process_examinationViews.html", context)

def techFileDirectoryViews(request):
    context = {}
    return render(request, "techdata/tech_file_directory.html", context)

def techInstallWeldViews(request):
    context = {}
    return render(request, "techdata/tech_install_weld.html", context)

def techHotDeelViews(request):
    context = {}
    return render(request, "techdata/tech_hot_deel.html", context)

def techTestPresureViews(request):
    context = {}
    return render(request, "techdata/tech_test_presure.html", context)

def techBoxMaterialViews(request):
    context = {}
    return render(request, "techdata/tech_box_material.html", context)

def techBoxWeldViews(request):
    context = {}
    return render(request, "techdata/tech_box_weld.html", context)

def techBoxOutboughtViews(request):
    context = {}
    return render(request, "techdata/tech_box_outbought.html", context)

def designBOMViews(request):
    """
    mxl
    """
    work_order_form = WorkOrderForm()
    context = {
        "form" : work_order_form
    }
    return render(request, "techdata/designBOM.html", context)

def connectionOrientationEditViews(request):
    context = {}
    return render(request, "techdata/connection_orientation_edit.html", context)

def firstFeedingViews(request):
    context = {}
    return render(request, "techdata/first_feeding.html", context)

def principalMaterialViews(request):
    context = {}
    return render(request, "techdata/principal_material.html", context)

def auxiliaryMaterialViews(request):
    context = {}
    return render(request, "techdata/auxiliary_material.html", context)

def processBOMViews(request):
    """
    JunHU
    """
    work_order_form = WorkOrderForm()
    context = {
        "form": work_order_form,
    }
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
