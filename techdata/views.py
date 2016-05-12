# coding: UTF-8
from django.shortcuts import render, redirect
from const.forms import InventoryTypeForm
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
import json, datetime, xlrd
from django.db import transaction
from django.contrib.auth.models import User
from backend.utility import getContext
from techdata.forms import *
from const.models import Materiel
from techdata.models import TransferCard, Program, WeldJointTech
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
    """
    JunHU
    """
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

def cooperantViews(request):
    """
    JunHU
    """
    work_order_form = WorkOrderForm()
    context = {
        "work_order_form" : work_order_form,
        "inventory_type": COOPERANT,
    }
    return render(request, "techdata/cooperant.html", context)

def outPurchasedViews(request):
    """
    JunHU
    """
    work_order_form = WorkOrderForm()
    context = {
        "work_order_form" : work_order_form,
        "inventory_type": OUT_PURCHASED,
    }
    return render(request, "techdata/out_purchased.html", context)

def firstFeedingViews(request):
    """
    JunHU
    """
    work_order_form = WorkOrderForm()
    context = {
        "work_order_form" : work_order_form,
        "inventory_type": FIRST_FEEDING,
    }
    return render(request, "techdata/first_feeding.html", context)

def principalMaterialViews(request):
    """
    JunHU
    """
    work_order_form = WorkOrderForm()
    principal_form = PrincipalItemForm()
    context = {
        "work_order_form" : work_order_form,
        "inventory_type": MAIN_MATERIEL,
        "principal_form": principal_form,
    }
    return render(request, "techdata/principal_material.html", context)

def auxiliaryMaterialViews(request):
    work_order_form = WorkOrderForm()
    context = {
        "work_order_form" : work_order_form,
        "inventory_type": AUXILIARY_MATERIEL,

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
    work_order_form = WorkOrderForm()
    context = {
        "form": work_order_form,
    }
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

def transferCardPicUpload(request):
    if request.is_ajax():
        if request.FILES['pic_file'].size > 10*1024*1024:
            file_upload_error = 2
        else:
            iid = request.POST['iid']
            card = TransferCard.objects.get(materiel_belong__id = iid)
            card.file_obj = request.FILES['pic_file']
            card.save()
            file_upload_error = 1
        return HttpResponse(json.dumps({"file_upload_error": file_upload_error, }))

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
    """
    BinWu
    """
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

def uploadHeatArrangement(request):
    """
    BinWu
    """
    if request.is_ajax():
        uf = UploadForm(request.POST, request.FILES)
        if uf.is_valid():
            card_id = request.GET.get("card_id")
            card = HeatTreatmentTechCard.objects.get(id=card_id)
            if HeatTreatmentArrangement.objects.filter(card_belong = card).count() == 0:
                HeatTreatmentArrangement(card_belong = card).save()
            card.heattreatmentarrangement.file_obj = uf.cleaned_data['pic']
            print(card.heattreatmentarrangement.file_obj.path)
            card.heattreatmentarrangement.save()
            return HttpResponse(card.heattreatmentarrangement.file_obj.path)


def techInstallWeldCard(request):
    """
    JunHU
    """
    iid = request.GET.get("iid")
    context = {
        "iid": iid,
    }
    return render(request, "techdata/tech_install_weld_card.html", context)

def connectOrientationAdd(request):
    """
    mxl
    """
    if request.is_ajax():
        if request.FILES['connectOrientation_file'].size > 10*1024*1024:
            file_upload_error = 2
        else:
            work_order_id = request.POST['work_order_id']
            print "cao"
            print work_order_id
            work_order = WorkOrder.objects.get(id = work_order_id)
            file = ConnectOrientation()
            file.order = work_order
            file.name = request.FILES['connectOrientation_file'].name
            file.file_obj = request.FILES['connectOrientation_file']
            file.file_size = str(int(request.FILES['connectOrientation_file'].size) / 1000) + "kb"
            file.upload_date = datetime.datetime.now()
            file.save()
            file_upload_error = 1

        return HttpResponse(json.dumps({'file_upload_error' : file_upload_error}))

def gen_material(name):
    try:
        name = int(name)
    except:
        pass
    target = Material.objects.filter(name = name)
    if target.count():
        return target[0]
    else:
        item = Material(name = name)
        item.save()
        return item

def BOMadd(request):
    """
    JunHU
    """
    if request.is_ajax():
        if request.FILES['BOM_file'].size > 10*1024*1024:
            file_upload_error = 2
        else:
            file = request.FILES['BOM_file']
            work_order_id = request.POST['work_order_id']
            work_order = WorkOrder.objects.get(id = work_order_id)
            book = xlrd.open_workbook(file_contents = file.read())
            table = book.sheets()[0]
            total = Materiel.objects.filter(order = work_order).count() + 1
            materiel_list = []
            
            
            #处理部件
            try:
                weight = float(table.cell(2, 5).value)
            except:
                try:
                    weight = float(table.cell(2, 6).value)
                except:
                    weight = None
            if total != 1:
                main_materiel = Materiel.objects.get(schematic_index = table.cell(2, 1).value)
                origin_count = int(main_materiel.count)
                materiel_list.append(Materiel(order = work_order, 
                                             index = 0, 
                                             sub_index = 0,
                                             schematic_index = table.cell(2, 1).value,
                                             parent_schematic_index = main_materiel.parent_schematic_index,
                                             parent_name = main_materiel.parent_name,
                                             name = table.cell(2, 2).value,
                                             material = gen_material(table.cell(2, 4).value),
                                             count = origin_count,
                                             net_weight = weight,
                                             remark = table.cell(2, 8).value,
                                    ))
            else:
                origin_count = 1
                materiel_list.append(Materiel(order = work_order, 
                                             index = total,
                                             sub_index = 0, 
                                             schematic_index = table.cell(2, 1).value,
                                             name = table.cell(2, 2).value,
                                             material = gen_material(table.cell(2, 4).value),
                                             count = origin_count, 
                                             net_weight = weight,
                                             remark = table.cell(2, 8).value,
                                    ))
                total += 1#产品总部件需要分配票号

            #处理零件
            for rownum in xrange(4, table.nrows):
                try:
                    weight = float(table.cell(rownum, 5).value)
                except:
                    try:
                        weight = float(table.cell(rownum, 6).value)
                    except:
                        weight = None
                materiel_list.append(Materiel(order = work_order, 
                                             index = total, 
                                             sub_index = int(table.cell(rownum, 0).value),
                                             schematic_index = table.cell(rownum, 1).value,
                                             parent_schematic_index = table.cell(2, 1).value,
                                             parent_name = table.cell(2, 2).value,
                                             name = table.cell(rownum, 2).value,
                                             material = gen_material(table.cell(rownum, 4).value),
                                             count = int(table.cell(rownum, 3).value) * origin_count, 
                                             net_weight = weight,
                                             remark = table.cell(rownum, 8).value
                                    ))
                total += 1
            for item in materiel_list:
                item.save()
                CirculationRoute(materiel_belong = item).save()
                Processing(materiel_belong = item).save()

            file_upload_error = 1
        return HttpResponse(json.dumps({'file_upload_error' : file_upload_error}))


def weldJointTechView(request, orderid):
    print "hehe"
    order = WorkOrder.objects.get(id = orderid)
    if WeldJointTech.objects.filter(order__id = orderid).count() == 0:
        weld_joint = WeldJointTech(order = order)
        weld_joint.save()
    else:
        weld_joint = WeldJointTech.objects.filter(order__id = orderid)[0]
    #weld_joint_details = WeldJointTechDetail.objects.filter(weld_joint = weld_joint, is_save = True)
    weld_joint_details = WeldJointTechDetail.objects.filter(Q(weld_joint = weld_joint) & Q(is_save = True))
    print len(weld_joint_details)
    context = {
        "weld_joint_index" : weld_joint.index,
        "weld_joint_details" : weld_joint_details,
    }
    return render(request, "techdata/weld_joint.html", context)
