# coding: UTF-8
from django.shortcuts import render, redirect
from const.forms import InventoryTypeForm
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
import json, datetime
from django.db import transaction
from django.contrib.auth.models import User
from backend.utility import getContext
from techdata.forms import *
from const.models import Materiel
from techdata.models import TransferCard, Program
from purchasing.models import MaterielExecute
from const.forms import WorkOrderForm

def techPreparationPlanViews(request):
    work_order_form = WorkOrderForm()
    context = {"work_order_form" : work_order_form}
    return render(request, "techdata/tech_preparation_plan.html", context)

def processExaminationViews(request):
    """
    MH Chen
    """
    form = WorkOrderForm()
    context = {
            "form": form,
    }
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
    #materiel_form = MaterielForm()
    #circulationroute_form = CirculationRouteForm()
    work_order_form = WorkOrderForm()
    context = {
        "work_order_form" : work_order_form
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
    categories_form = CategoriesForm()
    context = {
            "categories_form":categories_form
    }
    return render(request, "techdata/auxiliary_material.html", context)

def processBOMViews(request):
    """
    JunHU
    """
    work_order_form = WorkOrderForm()
    process_form = ProcessingForm()
    context = {
        "form": work_order_form,
        "process_form": process_form,
    }
    return render(request, "techdata/processBOM.html", context)

def weldListViews(request):
    """
    JunHU
    """
    work_order_form = WorkOrderForm()
    context = {
        "form": work_order_form,
    }
    return render(request, "techdata/weld_list.html", context)

def transferCardEditViews(request):
    """
    JunHU
    """
    iid = request.GET.get("iid")
    context = {
        "iid": iid,
    }
    cards = TransferCard.objects.filter(materiel_belong__id = iid)   
    if cards.count() == 0:
        context["form"] = TransferCardForm()

    return render(request, "techdata/transfer_card_edit.html", context)

def weldQuotaViews(request):
    context = {}
    return render(request, "techdata/weld_quota.html", context)
def weldEditViews(request):
    context = {}
    return render(request, "techdata/weld_edit.html", context)

def programmeEditViews(request):
    form = ProgramFeedbackForm()
    context = {
        "form": form,
    }
    return render(request, "techdata/programme_edit.html", context)

def programAdd(request):
    if request.is_ajax():
        if request.FILES['program_file'].size > 10*1024*1024:
            file_upload_error = 2
        else:
            execute_id = request.POST['execute_id']
            execute = MaterielExecute.objects.get(id = execute_id)
            file = Program()
            file.execute = execute
            file.file_obj = request.FILES['program_file']
            file.file_size = str(int(request.FILES['program_file'].size) / 1000) + "kb"
            file.name = request.FILES['program_file'].name
            file.upload_time = datetime.datetime.now()
            file.save()
            file_upload_error = 1
        return HttpResponse(json.dumps({"file_upload_error": file_upload_error, }))

def techDetailTableViews(request):
    """BinWu"""
    work_order_form = WorkOrderForm()
    context = {
        "form": work_order_form,
    }
    return render(request, "techdata/detail_table.html", context)

def heatTreatmentTechCardEditViews(request):
    """
    JunHU
    """
    card_id = request.GET.get("card_id");
    context = {
        "card_id": card_id,
    }
    return render(request, "techdata/heat_treatment_tech_card_edit.html", context)

def heatPoint(request):
    """
    BinWu
    """
    card_id = request.GET.get("card_id")
    context = {
        "card_id" : card_id,
    }
    return render(request, "techdata/heat_point.html",context)
