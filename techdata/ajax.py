#!/usr/bin/env python
# coding=utf-8

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.utils import simplejson

from django.db.models import Q
from django.contrib.auth.models import User

from const import *
from backend.utility import getContext, transferCardProcessPaginator
from const.models import *
from forms import MaterielForm

from techdata.forms import *
from techdata.models import *
from const.models import *
from const.utils import getMaterialQuerySet
from techdata.utility import batchDecentialization, processDetailGenerate

from purchasing.models import MaterielExecute, MaterielExecuteDetail
import datetime, re


def markGenerateFactory(order, inventory_type):
    """
    JunHU
    """
    if inventory_type == OUT_PURCHASED:
        return order.outpurchasedmark
    elif inventory_type == FIRST_FEEDING:
        return order.firstfeedingmark
    elif inventory_type == COOPERANT:
        return order.cooperantmark
    elif inventory_type == MAIN_MATERIEL:
        return order.principalmark
    elif inventory_type == AUXILIARY_MATERIEL:
        return order.auxiliarymark
    

def detailItemGenerateFactory(inventory_type):
    """
    JunHU
    """
    if inventory_type == OUT_PURCHASED:
        return OutPurchasedItem
    elif inventory_type == FIRST_FEEDING:
        return FirstFeedingItem
    elif inventory_type == COOPERANT:
        return CooperantItem
    elif inventory_type == MAIN_MATERIEL:
        return PrincipalItem

@dajaxice_register
def detailMark(request, id_work_order, step, inventory_type):
    """
    JunHU
    """
    order = WorkOrder.objects.get(id = id_work_order)
    DetailItem = detailItemGenerateFactory(inventory_type)
    mark = markGenerateFactory(order, inventory_type)
    if step == MARK_WRITE:
        mark.writer = request.user
        mark.write_date = datetime.datetime.today()
        mark.save()
        context = {
            "ret": True,
            "mark_user": unicode(mark.writer.userinfo),
        }
    elif step == MARK_REVIEW:
        mark.reviewer = request.user
        mark.review_date = datetime.datetime.today()
        mark.save()
        batchDecentialization(order, inventory_type, DetailItem)
        context = {
            "ret": True,
            "mark_user": unicode(mark.reviewer.userinfo),
        }
    else:
        context = {
            "ret": False,
            "warning": u"后台保存错误"
        }
    return simplejson.dumps(context)
def detailItemGenerateFactory(inventory_type):
    """
    JunHU
    """
    if inventory_type == OUT_PURCHASED:
        return OutPurchasedItem
    elif inventory_type == FIRST_FEEDING:
        return FirstFeedingItem
    elif inventory_type == COOPERANT:
        return CooperantItem
    elif inventory_type == MAIN_MATERIEL:
        return PrincipalItem
    elif inventory_type == AUXILIARY_MATERIEL:
        return AuxiliaryItem

@dajaxice_register
def getInventoryTables(request, id_work_order, inventory_type):
    """
    JunHU
    """
    id2table = {
        OUT_PURCHASED: "out_purchased_table.html",
        FIRST_FEEDING: "first_feeding_table.html",
        COOPERANT: "cooperant_table.html",
        MAIN_MATERIEL: "principal_material_table.html",
        AUXILIARY_MATERIEL:"auxiliary_material_table.html",
    }
    work_order = WorkOrder.objects.get(id = id_work_order)
    DetailItem = detailItemGenerateFactory(inventory_type)
    context = {
        "MARK_WRITE": MARK_WRITE,
        "MARK_REVIEW": MARK_REVIEW,
        "work_order": work_order,
    }
    if inventory_type == MAIN_MATERIEL:
        list = DetailItem.objects.filter(order = work_order)
    else:
        list = DetailItem.objects.filter(materiel_belong__order = work_order)
    context["list"] = list
    html = render_to_string("techdata/widgets/" + id2table[inventory_type], context)
    return html

@dajaxice_register
def deleteSingleItem(request, iid, inventory_type):
    DetailItem = detailItemGenerateFactory(inventory_type)
    item = DetailItem.objects.get(id = iid)
    item.delete()

@dajaxice_register
def getItemInfo(request, iid, inventory_type):
    """
    JunHU
    """
    DetailItem = detailItemGenerateFactory(inventory_type)
    item = DetailItem.objects.get(id = iid)
    if inventory_type == MAIN_MATERIEL:
        principal_form = PrincipalItemForm(instance = item)
        html = render_to_string("techdata/widgets/principal_card.html", {"principal_form": principal_form})
    else:
        html = ""
    return html

@dajaxice_register
def updateDetailItemInfo(request, remark, iid, inventory_type):
    DetailItem = detailItemGenerateFactory(inventory_type)
    item = DetailItem.objects.get(id = iid)
    item.remark = remark
    item.save()

@dajaxice_register
def addOrUpdateSinglePrincipalItem(request, id_work_order, form, iid = None):
    if iid == None:
        form = PrincipalItemForm(deserialize_form(form))
        work_order = WorkOrder.objects.get(id = id_work_order)
        if form.is_valid():
            item = form.save(commit = False)
            item.order = work_order
            item.save()
            return "ok"
        return "fail"
    else:
        item = PrincipalItem.objects.get(id = iid)
        form = PrincipalItemForm(deserialize_form(form), instance = item)
        if form.is_valid():
            form.save()
            return "ok"
        return "fail"

@dajaxice_register
def addSingleItem(request, id_work_order, index, inventory_type):
    """
    JunHU
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    DetailItem = detailItemGenerateFactory(inventory_type)
    item = Materiel.objects.filter(Q(index = index) & Q(order = work_order))
    if item.count() == 0:
        context = {"success": False, "remark": u"未查到该票号零件"}
        return simplejson.dumps(context)
    item = item[0]
    if DetailItem.objects.filter(materiel_belong = item).count() > 0:
        context = {"success": False, "remark": u"该零件已添加至明细中"}
        return simplejson.dumps(context)
    DetailItem(materiel_belong = item).save()
    context = {"success" : True, "remark": u"添加成功"}
    return simplejson.dumps(context)

@dajaxice_register
def autoSetInventoryLabel(request, id_work_order, inventory_type):
    """
    JunHU
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    DetailItem = detailItemGenerateFactory(inventory_type)
    if inventory_type == OUT_PURCHASED:
        for item in Materiel.objects.filter(order = work_order):
            if item.sub_index == "0" and item.index != "1": continue
            if not item.route().startswith("GY"): continue
            if item.schematic_index and item.schematic_index.endswith(".00"): continue
            if DetailItem.objects.filter(materiel_belong = item).count() > 0: continue
            DetailItem(materiel_belong = item, remark = item.remark).save()
    elif inventory_type == FIRST_FEEDING:
        for item in Materiel.objects.filter(order = work_order):
            if item.sub_index == "0" and item.index != "1": continue
            if not (item.route().startswith("DY") or item.route().startswith("H1.XZ.H1")): continue
            if DetailItem.objects.filter(materiel_belong = item).count() > 0: continue
            DetailItem(materiel_belong = item, remark = item.remark).save()
    elif inventory_type == COOPERANT:
        for item in Materiel.objects.filter(order = work_order):
            if item.sub_index == "0" and item.index != "1": continue
            if not item.route().startswith("H1.J"): continue
            if DetailItem.objects.filter(materiel_belong = item).count() > 0: continue
            DetailItem(materiel_belong = item, remark = item.remark).save()
    elif inventory_type == AUXILIARY_MATERIEL:
        for item in Materiel.objects.filter(order = work_order):
            if item.sub_index == "0" and item.index != "1": continue
            if not item.route().startswith("H1"): continue
            if item.schematic_index and item.schematic_index.endswith(".00"): continue
            if DetailItem.objects.filter(materiel_belong = item).count() > 0: continue
            DetailItem(materiel_belong = item, remark = item.remark).save()

@dajaxice_register
def getProcessBOM(request, id_work_order):
    """
    JunHU
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    BOM = Materiel.objects.filter(order = work_order)
    for item in BOM:
        if item.processing.GX1 == None:
            continue
        for i in xrange(1, 13):
            step = getattr(item.processing, "GX%d" % i)
            if step == None:
                break
            setattr(item, "GX%d" % i, step)

    context = {
        "work_order": work_order,
        "BOM": BOM,
        "MARK_WRITE": MARK_WRITE,
        "MARK_PROOFREAD": MARK_PROOFREAD,
        "MARK_STATISTIC": MARK_STATISTIC,
        "MARK_QUOTA": MARK_QUOTA,
    }
    html = render_to_string("techdata/widgets/processBOM_table.html", context)
    return html

@dajaxice_register
def getSingleProcessBOM(request, iid):
    """
    JunHU
    """
    item = Materiel.objects.get(id = iid)
    context = {
        "item": item,
    }
    html = render_to_string("techdata/widgets/processBOM_row.html", context)
    html2 = render_to_string("techdata/widgets/processBOM_row_2.html", context)
    return simplejson.dumps({"html": html, "html2": html2, })

@dajaxice_register  
def getAuxiliaryMaterielInfo(request, iid,categories):
    """
    MH Chen
    """
    materiel = Materiel.objects.get(id = iid)
    form = AuxiliaryMaterielForm(instance = materiel)
    categories_form = CategoriesForm(initial={"categorie_type":categories})
    try:
        user_ratio = 0
        if materiel.net_weight != None and materiel.quota != None:
            user_ratio = round(materiel.net_weight/materiel.quota,5)
    except:
        pass
    context = {
        "categories_form":categories_form,
        "form": form,
        "user_ratio":user_ratio,
    }
    html = render_to_string("techdata/widgets/auxiliary_material_type_in.html", context)
    return html


@dajaxice_register  
def getMaterielInfo(request, iid):
    """
    JunHU
    """
    materiel = Materiel.objects.get(id = iid)
    form = MaterielForm(instance = materiel)
    context = {
        "form": form,
    }
    html = render_to_string("techdata/widgets/materiel_base_info.html", context)
    return html  

@dajaxice_register  
def getMaterielDetailInfo(request, iid):
    """
    MH Chen
    """

    materiel = AuxiliaryItem.objects.get( id = iid).materiel_belong
    context = {
        "materiel": materiel,
    }
    html = render_to_string("techdata/widgets/auxiliary_material_base_info_table.html", context)
    return html  

@dajaxice_register  
def getTechdataList(request, id_work_order):
    """
    MH Chen
    """
    workorder = WorkOrder.objects.get(id = id_work_order)
    review_list = ProcessReview.objects.filter(materiel__order = workorder)
    context = {
        "workorder": workorder,
        "review_list":review_list,
    }
    html = render_to_string("techdata/widgets/process_examination_table.html", context)
    return html

@dajaxice_register  
def getIndex(request, index):
    """
    MH Chen
    """
    if(index!=""):
        materiel_list = Materiel.objects.filter(index__icontains = index)
        
        
    context = { 
            "materiel_list": materiel_list,
    }
    html = render_to_string("techdata/widgets/process_examination_table2.html", context)
    return html 

@dajaxice_register  
def addProcessReview(request,materiel_name,problem_statement,advice_statement):
    """
    MH Chen
    """
    materiel = Materiel.objects.get(name = materiel_name)
    processReview = ProcessReview (materiel = materiel, problem_statement = problem_statement,advice_statement=advice_statement)
    processReview.save()        

@dajaxice_register
def getProcess(request, iid):
    """
    JunHU
    """
    materiel = Materiel.objects.get(id = iid)
    form = ProcessingRouteForm(instance = materiel.processing)
    context = {
        "form": form,
    }
    html = render_to_string("techdata/widgets/process_table.html", context)
    return html
@dajaxice_register
def getAuxiliary(request, iid):
    """
    MH Chen
    """
    
    materiel = AuxiliaryItem.objects.get( id = iid).materiel_belong
    form = AuxiliaryForm(instance = materiel.auxiliaryitem)
    context = {
        "form": form,
    }
    html = render_to_string("techdata/widgets/auxiliary_material_form.html", context)
    return html

@dajaxice_register
def getDesignBOM(request, id_work_order):
    """
    mxl
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    BOM = Materiel.objects.filter(order = work_order)
    context = {
        "work_order" : work_order,
        "BOM" : BOM,
    }
    if DesignBOMMark.objects.filter(order = work_order).count() == 0:
        DesignBOMMark(order = work_order).save()
    read_only = (work_order.designbommark.reviewer != None)
    html = render_to_string("techdata/widgets/designBOM_table.html", context)
    return simplejson.dumps({"read_only" : read_only, "html" : html})

@dajaxice_register
def getSingleDesignBOM(request, iid):
    """
    mxl
    """
    item = Materiel.objects.get(id = iid)
    context = {
        "item" : item
    }
    row_html = render_to_string("techdata/widgets/designBOM_row.html", context)
    return row_html

@dajaxice_register
def getDesignBOMForm(request, iid):
    """
    mxl
    """
    materiel = Materiel.objects.get(id = iid)
    circulationroute = CirculationRoute.objects.filter(materiel_belong = iid)[0]
    materiel_form = MaterielForm(instance = materiel)
    circulationroute_form = CirculationRouteForm(instance = circulationroute)
    materiel_form_html = render_to_string("techdata/widgets/designBOM_materiel_form.html", {'materiel_form' : materiel_form})
    circulationroute_form_html = render_to_string("techdata/widgets/designBOM_circulationroute_form.html", {'circulationroute_form' : circulationroute_form})
    return simplejson.dumps({'materiel_form' : materiel_form_html, 'circulationroute_form' : circulationroute_form_html})

@dajaxice_register
def getProcessReviewForm(request, iid):
    """
    MH Chen
    """
    processReview = ProcessReview.objects.get(id = iid)
    processReview_form = ProcessReviewForm(instance = processReview)
    html = render_to_string("techdata/widgets/processReview_form.html", {'processReview_form' : processReview_form})
    return html

@dajaxice_register
def getWeldSeamCard(request, full = False, iid = None):
    """
    JunHU
    """
    if iid:
        weld_seam = WeldSeam.objects.get(id = iid)
        form = WeldSeamForm(instance = weld_seam)
    else:
        form = WeldSeamForm()
    material_set = getMaterialQuerySet(WELD_ROD, WELD_WIRE)
    form.fields["weld_material_1"].queryset = material_set
    form.fields["weld_material_2"].queryset = material_set
    material_set = getMaterialQuerySet(WELD_FLUX)
    form.fields["weld_flux_1"].queryset = material_set
    form.fields["weld_flux_2"].queryset = material_set
    context = {
        "form": form,
    }
    html = render_to_string("techdata/widgets/weld_seam_full_card.html", context)
    return html
@dajaxice_register
def getWeldQuotaCard(request,iid = None):
    """
    MH Chen
    """
    if iid:
        weld_quota = WeldQuota.objects.get(id = iid)
        form = WeldQuotaForm(instance = weld_quota)
    else:
        form = WeldSeamForm()
    context = {
        "form": form,
        "weld_quota":weld_quota,
    }
    html = render_to_string("techdata/widgets/weld_quota_card.html", context)
    return html

@dajaxice_register
def boxOutBought(request, order):
    """
    BinWu
    """
    work_order = WorkOrder.objects.get(id = order)
    list = Materiel.objects.filter(order = order)
    context = {
        "list" : list,
        "work_order" : work_order,
    }
    html = render_to_string("techdata/widgets/tech_box_outbought_table.html", context)
    return html

@dajaxice_register
def firstFeeding(request, order):
    """
    BinWu
    """
    list = Materiel.objects.filter(order = order)
    context = {
        "list" : list,
    }
    html = render_to_string("techdata/widgets/first_feeding_table.html", context)
    return html

@dajaxice_register
def principalMaterial(request, order):
    """
    BinWu
    """
    list = Materiel.objects.filter(order = order)
    context = {
        "list" : list,
    }
    html = render_to_string("techdata/widgets/principal_material_table.html", context)
    return html

@dajaxice_register
def auxiliaryMaterial(request, order):
    """
    MH Chen 
    """
    work_order = WorkOrder.objects.get(id = order)
    list = Materiel.objects.filter(order = order)
    for item in list:
        try:
            item.user_ratio = round(item.net_weight / item.quota, 5)
        except:
            item.user_ratio = 0
    context = {
        "list" : list,
        "work_order":work_order,
    }
    html = render_to_string("techdata/widgets/auxiliary_material_table.html", context)
    return html

@dajaxice_register
def weldList(request, order):
    """
    BinWu
    """
    list = Materiel.objects.filter(order = order)
    context = {
        "list" : list,
    }
    html = render_to_string("techdata/widgets/weld_list_table.html", context)
    return html

@dajaxice_register
def techBoxWeld(request, order):
    """
    BinWu
    """
    list = Materiel.objects.filter(order = order)
    context = {
        "list" : list,
    }
    html = render_to_string("techdata/widgets/tech_box_weld_table.html", context)
    return html

@dajaxice_register
def updateAuxiliary(request,iid,form):
    """
    MH Chen
    """
    materiel = AuxiliaryItem.objects.get(id = iid).materiel_belong
    form = AuxiliaryForm(deserialize_form(form),instance = AuxiliaryItem.objects.get(materiel_belong = materiel))
    if form.is_valid():
        obj = form.save(commit = False)
        obj.materiel_belong = materiel
        obj.save()
        return "ok"

@dajaxice_register
def addWeldSeam(request, iid, form):
    """
    JunHU
    """
    materiel = Materiel.objects.get(id = iid)
    form = WeldSeamForm(deserialize_form(form))
    if form.is_valid():
        obj = form.save(commit = False)
        obj.materiel_belong = materiel
        obj.save()
        return "ok"
    else:
        context = {
            "form": form,
        }
        html = render_to_string("techdata/widgets/weld_seam_card.html", context)
        return html

@dajaxice_register
def modifyWeldSeam(request, iid, form):
    """
    JunHU
    """
    weldseam = WeldSeam.objects.get(id = iid)
    form = WeldSeamForm(deserialize_form(form), instance = weldseam)
    if form.is_valid():
        form.save()
        return "ok"
    else:
        context = {
            "form": form,
        }
        html = render_to_string("techdata/widgets/weld_seam_full_card.html", context)
        return html

@dajaxice_register
def getWeldSeamList(request, id_work_order):
    """
    JunHU
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    weldseam_list = WeldSeam.objects.filter(materiel_belong__order = work_order)
    context = {
        "weldseam_list": weldseam_list,
        "work_order": work_order,
    }
    html = render_to_string("techdata/widgets/weld_list_table.html", context)
    read_only = (work_order.weldlistpagemark.reviewer != None)

    return simplejson.dumps({"html": html, "read_only": read_only,})

@dajaxice_register
def getWeldQuotaList(request, id_work_order):
    """
    MH Chen
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    weld_quota_list = WeldQuota.objects.filter(order = work_order)
    context = {
        "weld_quota_list": weld_quota_list,
        "work_order": work_order,
    }
    html = render_to_string("techdata/widgets/weld_quota_table.html", context)
    read_only = (work_order.weldlistpagemark.reviewer != None)

    return simplejson.dumps({"html": html, "read_only": read_only,})
@dajaxice_register
def getWeldSeamWeight(request, id_work_order):
    """
    MH Chen
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    try:
        weld_quota_list = WeldQuota.objects.filter(order = work_order)
    except WeldQuota.DoesNotExist:
        pass
    context = {
        "work_order":work_order,
        "weld_quota_list":weld_quota_list,
    }
    html = render_to_string("techdata/widgets/weld_quota_table.html", context)
    return html
    
@dajaxice_register
def saveWeldQuota(request, id_work_order):
    """
    MH Chen
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    weldseam_list = WeldSeam.objects.filter(materiel_belong__order = work_order)
    dic = {}
    for item1 in weldseam_list:
        if item1.weld_material_1 != None:
            if dic.has_key((item1.weld_material_1,item1.size_1,item1.weld_material_1.get_categories_display)):
                dic[(item1.weld_material_1,item1.size_1,item1.weld_material_1.get_categories_display)]+= float(item1.weight_1)
            else:
                dic[(item1.weld_material_1,item1.size_1,item1.weld_material_1.get_categories_display)] = float(item1.weight_1)
    for item2 in weldseam_list:
        if item2.weld_material_2 != None:
            if dic.has_key((item2.weld_material_2,item2.size_2,item2.weld_material_2.get_categories_display)):
                dic[(item2.weld_material_2,item2.size_2,item2.weld_material_2.get_categories_display)]+= float(item2.weight_2)
            else:
                dic[(item2.weld_material_2,item2.size_2,item2.weld_material_2.get_categories_display)] = float(item2.weight_2)
    for item in dic:
        weldQuota = WeldQuota(order = work_order,weld_material = item[0],size = item[1],quota = dic[item])
        weldQuota.save()

    return "ok"
@dajaxice_register
def updateWeldQuota(request,form,work_order,iid):
    """
    MH Chen
    """
    print form
    order = WorkOrder.objects.get(id = work_order)
    quota_form = WeldQuotaForm(deserialize_form(form),instance = WeldQuota.objects.get(id = iid))
    print form
    if quota_form.is_valid():
        quota = quota_form.save(commit = False)
        quota.order = order
        quota.save()
        return  "ok"
    else:
        return "fail"

@dajaxice_register
def deleteWeldQuota(request,did):
    """
    MH Chen
    """
    weld_quota = WeldQuota.objects.get(id = did)
    weld_quota.delete()
    return "ok"
@dajaxice_register
def addWeldQuota(request,form,work_order):
    """
    MH Chen
    """
    order = WorkOrder.objects.get(id = work_order)
    quota_form = WeldQuotaForm(deserialize_form(form))
    if quota_form.is_valid():
        quota = quota_form.save(commit = False)
        quota.order = order
        quota.save()
        return  "ok"
    else:
        return "fail"
@dajaxice_register
def getMaterial(request,work_order):
    """
    MH Chen
    """
    order = WorkOrder.objects.get(id = work_order)
    form = WeldQuotaForm()
    context = {
        "form": form,
    }
    html = render_to_string("techdata/widgets/weld_quota_add_card.html", context)
    return html
@dajaxice_register  
def updateProcessReview(request, iid,processReview_form):
    """
    MH Chen
    """
    processReview = ProcessReview.objects.get(id = iid)
    processReview_form = ProcessReviewForm(deserialize_form(processReview_form),instance = processReview)
    if processReview_form.is_valid():
        processReview_form.save()
        return  "ok"
    else:
        return "fail"

@dajaxice_register
def getSingleWeldSeamInfo(request, iid):
    """
    JunHU
    """
    weldseam = WeldSeam.objects.get(id = iid)
    context = {
        "item": weldseam,
    }
    html = render_to_string("techdata/widgets/weld_row.html", context)
    return html

@dajaxice_register
def saveDesignBOM(request, iid,  materiel_form, circulationroute_form):
    """
    mxl
    """
    materiel = Materiel.objects.get(id = iid)
    circulationroute = CirculationRoute.objects.filter(materiel_belong = materiel)[0]
    materiel_form = MaterielForm(deserialize_form(materiel_form), instance = materiel)
    circulationroute_form = CirculationRouteForm(deserialize_form(circulationroute_form), instance = circulationroute)
    if materiel_form.is_valid() and circulationroute_form.is_valid():
        materiel_form.save()
        obj = circulationroute_form.save(commit = False)
        obj.materiel_belong = materiel
        obj.save()
        ret = {"status" : "ok"}
    else:
        ret = {
            "status" : "fail",
        }
        if not materiel_form.is_valid():
            html = render_to_string("techdata/widgets/designBOM_materiel_form.html", {"materiel_form" : materiel_form})
            ret["html"] = html
            ret["materiel_error"] = "1"
        if not circulationroute_form.is_valid():
            ret["circulationroute_error"] = "1"
    return simplejson.dumps(ret)

@dajaxice_register
def saveProcess(request, iid,  materiel_form, processing_form):
    """
    JunHU
    """
    materiel = Materiel.objects.get(id = iid)
    processingroute = Processing.objects.filter(materiel_belong = materiel)[0]
    materiel_form = MaterielForm(deserialize_form(materiel_form), instance = materiel)
    processing_form = ProcessingRouteForm(deserialize_form(processing_form), instance = processingroute)
    if materiel_form.is_valid() and processing_form.is_valid():
        materiel_form.save()
        obj = processing_form.save(commit = False)
        obj.materiel_belong = materiel
        obj.save()
        ret = {"status" : "ok"}
    else:
        ret = {
            "status" : "fail",
        }
        if not materiel_form.is_valid():
            html = render_to_string("techdata/widgets/materiel_base_info.html", {"form" : materiel_form})
            ret["html"] = html
            ret["materiel_error"] = "1"
        if not processing_form.is_valid():
            ret["processing_error"] = "1"
    return simplejson.dumps(ret)

@dajaxice_register
def weldListWriterConfirm(request, id_work_order):
    """
    JunHU
    """
    order = WorkOrder.objects.get(id = id_work_order)
    if WeldListPageMark.objects.filter(order = order).count() == 0:
        WeldListPageMark(order = order).save()
    order.weldlistpagemark.writer = request.user
    order.weldlistpagemark.write_date = datetime.datetime.today()
    order.weldlistpagemark.save()
    return simplejson.dumps({"ret": True, "user": unicode(request.user.userinfo)})

@dajaxice_register
def weldListReviewerConfirm(request, id_work_order):
    """
    JunHU
    """
    order = WorkOrder.objects.get(id = id_work_order)
    if WeldListPageMark.objects.filter(order = order).count() == 0:
        WeldListPageMark(order = order).save()

    if order.weldlistpagemark.writer == None:
        return simplejson.dumps({"ret": False})
    order.weldlistpagemark.reviewer = request.user
    order.weldlistpagemark.reviewe_date = datetime.datetime.today()
    order.weldlistpagemark.save()
    return simplejson.dumps({"ret": True, "user": unicode(request.user.userinfo)})

@dajaxice_register
def boxOutBoughtWriteConfirm(request, id_work_order):
    """
    BinWu
    """
    order = WorkOrder.objects.get(id = id_work_order)
    if BoxOutBoughtMark.objects.filter(order = order).count() == 0:
        BoxOutBoughtMark(order = order).save()
    order.boxoutboughtmark.writer = request.user
    order.boxoutboughtmark.write_date = datetime.datetime.today()
    order.boxoutboughtmark.save()
    return simplejson.dumps({"ret": True, "user": unicode(request.user.userinfo)})


@dajaxice_register
def boxOutBoughtReviewConfirm(request, id_work_order):
    """
    BinWu
    """
    order = WorkOrder.objects.get(id = id_work_order)
    if BoxOutBoughtMark.objects.filter(order = order).count() == 0:
        BoxOutBoughtMark(order = order).save()

    if order.boxoutboughtmark.writer == None:
        return simplejson.dumps({"ret": False})
    order.boxoutboughtmark.reviewer = request.user
    order.boxoutboughtmark.review_date = datetime.datetime.today()
    order.boxoutboughtmark.save()
    return simplejson.dumps({"ret": True, "user": unicode(request.user.userinfo)})

@dajaxice_register
def processBOMMark(request, id_work_order, step):
    """
    JunHU
    """
    order = WorkOrder.objects.get(id = id_work_order)
    if step == MARK_WRITE:
        order.processbompagemark.writer = request.user
        order.processbompagemark.write_date = datetime.datetime.today()
        order.processbompagemark.save()
        context = {
            "ret": True,
            "mark_user": unicode(order.processbompagemark.writer.userinfo),
        }
    elif step == MARK_STATISTIC:
        order.processbompagemark.statistician = request.user
        order.processbompagemark.statistic_date = datetime.datetime.today()
        order.processbompagemark.save()
        context = {
            "ret": True,
            "mark_user": unicode(order.processbompagemark.statistician.userinfo),
        }
    elif step == MARK_QUOTA:
        order.processbompagemark.quota_agent = request.user
        order.processbompagemark.quota_date = datetime.datetime.today()
        order.processbompagemark.save()
        context = {
            "ret": True,
            "mark_user": unicode(order.processbompagemark.quota_agent.userinfo),
        }
    elif step == MARK_PROOFREAD:
        order.processbompagemark.proofreader = request.user
        order.processbompagemark.proofread_date = datetime.datetime.today()
        order.processbompagemark.save()
        processDetailGenerate(order)
        context = {
            "ret": True,
            "mark_user": unicode(order.processbompagemark.proofreader.userinfo),
        }
    else:
        context = {
            "ret": False,
            "warning": u"后台保存错误"
        }
    return simplejson.dumps(context)

@dajaxice_register
def createTransferCard(request, iid, card_type):
    """
    JunHU
    """
    item = Materiel.objects.get(id = iid)
    card = TransferCard(materiel_belong = item, card_type = card_type)
    card.materiel_belong = item
    card.card_type = card_type
    card.file_index = "%02d" % (TransferCard.objects.filter(Q(materiel_belong__order = item.order) & Q(card_type = card_type)).count() + 1)
    card.save()
    mark = TransferCardMark(card = card)
    mark.save()


@dajaxice_register
def getTransferCard(request, iid, page = "1", is_print = False):
    """
    JunHU
    """
    item = Materiel.objects.get(id = iid)
    
    context = {
        "item": item,
        "MARK_WRITE": MARK_WRITE,
        "MARK_REVIEW": MARK_REVIEW,
        "MARK_PROOFREAD": MARK_PROOFREAD,
        "MARK_APPROVE": MARK_APPROVE,
        "CYLIDER_TRANSFER_CARD": CYLIDER_TRANSFER_CARD,
        "CAP_TRANSFER_CARD": CAP_TRANSFER_CARD,
        "WELD_TEST_PLATE_CARD": WELD_TEST_PLATE_CARD,
        "PARENT_TEST_PLATE_CARD": PARENT_TEST_PLATE_CARD,
        "is_print": is_print,
    }
    card = TransferCard.objects.get(materiel_belong = item)
    context["card"] = card
    process_list = TransferCardProcess.objects.filter(card_belong = card)
    if card.card_type == CYLIDER_TRANSFER_CARD or card.card_type == CAP_TRANSFER_CARD:
        page = int(page)
        page, total_page, process_list = transferCardProcessPaginator(process_list, page, 82, 8, 15)
        context["total_page"] = total_page
        context["current_page"] = page
        context["process_list"] = process_list
    elif card.card_type == PARENT_TEST_PLATE_CARD or card.card_type == WELD_TEST_PLATE_CARD:
        page, total_page, process_list = transferCardProcessPaginator(process_list, page, 100, 7, 7)
        
        context["total_page"] = total_page
        context["current_page"] = page

        context["process_list"] = process_list

        if card.card_type == PARENT_TEST_PLATE_CARD:
            context["test_type"] = "母材"
        if card.card_type == WELD_TEST_PLATE_CARD:
            context["test_type"] = "试板"
    elif card.card_type == PRESSURE_PART_TRANSFER_CARD or card.card_type == SPECIAL_PART_TRANSFER_CARD:
        page = int(page)
        page, total_page, process_list = transferCardProcessPaginator(process_list, page, 82, 12, 12)
        context["total_page"] = total_page
        context["current_page"] = page

        context["process_list"] = process_list

    html = render_to_string(CARD_TYPE_TO_HTML[card.card_type], context)
    return html

@dajaxice_register
def getTransferCardProcessList(request, iid):
    """
    JunHU
    """
    card = TransferCard.objects.get(materiel_belong__id = iid)
    print card.card_type
    process_list = TransferCardProcess.objects.filter(card_belong = card)
    context = {
        "process_list": process_list,
    }
    if card.card_type == CYLIDER_TRANSFER_CARD or card.card_type == CAP_TRANSFER_CARD or \
       card.card_type == PRESSURE_PART_TRANSFER_CARD or card.card_type == SPECIAL_PART_TRANSFER_CARD:
        context["has_process_name"] = True
    html = render_to_string("techdata/widgets/transfercard_process_list.html", context)
    return html

@dajaxice_register
def importTransferCardProcessTemplate(request, iid):
    """
    JunHU
    """
    card = TransferCard.objects.get(materiel_belong__id = iid)
    card.transfercardprocess_set.all().delete()
    
    process_list = []
    template = {
        CYLIDER_TRANSFER_CARD: cyliderProcessTemplate,
        CAP_TRANSFER_CARD: capProcessTemplate,
    }[card.card_type]

    for item in template:
        process_list.append(TransferCardProcess(card_belong = card, index = item["index"], name = item["name"], detail = item["detail"]))

    TransferCardProcess.objects.bulk_create(process_list)
    process_list = TransferCardProcess.objects.filter(card_belong = card)

    context = {
        "process_list": process_list,
    }
    if card.card_type == CYLIDER_TRANSFER_CARD or card.card_type == CAP_TRANSFER_CARD or \
       card.card_type == PRESSURE_PART_TRANSFER_CARD or card.card_type == SPECIAL_PART_TRANSFER_CARD:
        context["has_process_name"] = True

    html = render_to_string("techdata/widgets/transfercard_process_list.html", context)
    return html
   
@dajaxice_register
def addTransferCardProcess(request, iid):
    """
    JunHU
    """
    card = TransferCard.objects.get(materiel_belong__id = iid)
    TransferCardProcess(card_belong = card).save()
    process_list = TransferCardProcess.objects.filter(card_belong = card)
    context = {
        "process_list": process_list,
    }
    if card.card_type == CYLIDER_TRANSFER_CARD or card.card_type == CAP_TRANSFER_CARD or \
       card.card_type == PRESSURE_PART_TRANSFER_CARD or card.card_type == SPECIAL_PART_TRANSFER_CARD:
        context["has_process_name"] = True

    html = render_to_string("techdata/widgets/transfercard_process_list.html", context)
    return html

@dajaxice_register
def saveTransferCardRequirement(request, iid, requirement):
    card = TransferCard.objects.get(materiel_belong__id = iid)
    card.tech_requirement = requirement
    card.save()

@dajaxice_register
def saveTransferCardProcess(request, arr):
    """
    JunHU
    """
    for item in arr:
        process = TransferCardProcess.objects.get(id = item.get("pid", None))
        process.index = item.get("index", None)
        process.name = item.get("name", None)
        process.detail = item.get("detail", None)
        process.save()

@dajaxice_register
def removeTransferCardProcess(request, pid):
    """
    JunHU
    """
    process = TransferCardProcess.objects.get(id = pid)
    process.delete()

@dajaxice_register
def getTransferCardInfoForm(request, iid):
    """
    JunHU
    """
    card = TransferCard.objects.get(materiel_belong__id = iid)
    form = TransferCardInfoForm(instance = card)
    html = render_to_string("techdata/widgets/transfer_card_info_card.html", {"form": form, })
    return html

@dajaxice_register
def saveTransferCardInfoForm(request, iid, form):
    """
    JunHU
    """
    card = TransferCard.objects.get(materiel_belong__id = iid)
    form = TransferCardInfoForm(deserialize_form(form), instance = card)
    if form.is_valid():
        form.save()
        return simplejson.dumps({"ret": "ok"})
    else:
        html = render_to_string("techdata/widgets/transfer_card_info_card.html", {"form": form, })
        return simplejson.dumps({"ret": "fail", "html": html})

@dajaxice_register
def transferCardMark(request, iid, step):
    """
    JunHU
    """
    def date2str(date):
        return str(date.year) + "." + "%02d" % date.month + "." + str(date.day)
    
    item = Materiel.objects.get(id = iid)
    context = {}
    if step == MARK_WRITE:
        card = TransferCard.objects.get(materiel_belong = item)
        card.transfercardmark.writer = request.user
        card.transfercardmark.write_date = datetime.datetime.today()
        card.transfercardmark.save()
        context = {
            "ret": True,
            "file_index": unicode(card),
            "mark_user": unicode(card.transfercardmark.writer.userinfo),
            "mark_date": date2str(card.transfercardmark.write_date)
        }
    elif step == MARK_PROOFREAD:
        card = TransferCard.objects.get(materiel_belong = item)
        if card.transfercardmark.writer == None:
            context = {
                "ret": False,
                "warning": u"该流转卡还未完成编制",
            }
            return simplejson.dumps(context)

        card.transfercardmark.proofreader = request.user
        card.transfercardmark.proofread_date = datetime.datetime.today()
        card.transfercardmark.save()
        context = {
            "ret": True,
            "mark_user": unicode(card.transfercardmark.proofreader.userinfo),
            "mark_date": date2str(card.transfercardmark.proofread_date)
        }
    elif step == MARK_REVIEW:
        card = TransferCard.objects.get(materiel_belong = item)
        if card.transfercardmark.proofreader == None:
            context = {
                "ret": False,
                "warning": u"该流转卡还未完成校对",
            }
            return simplejson.dumps(context)

        card.transfercardmark.reviewer = request.user
        card.transfercardmark.review_date = datetime.datetime.today()
        card.transfercardmark.save()
        context = {
            "ret": True,
            "mark_user": unicode(card.transfercardmark.reviewer.userinfo),
            "mark_date": date2str(card.transfercardmark.review_date)
        }
    elif step == MARK_APPROVE:
        card = TransferCard.objects.get(materiel_belong = item)
        if card.transfercardmark.reviewer == None:
            context = {
                "ret": False,
                "warning": u"该流转卡还未完成审核",
            }
            return simplejson.dumps(context)

        card.transfercardmark.approver = request.user
        card.transfercardmark.approve_date = datetime.datetime.today()
        card.transfercardmark.save()
        context = {
            "ret": True,
            "mark_user": unicode(card.transfercardmark.approver.userinfo),
            "mark_date": date2str(card.transfercardmark.approve_date)
        }
    else:
        context = {
            "ret": False,
            "warning": u"后台保存出错",
        }
    return simplejson.dumps(context)

@dajaxice_register
def getTransferCardList(request, id_work_order):
    """
    JunHU
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    card_list = TransferCard.objects.filter(materiel_belong__order = work_order)
    context = {
        "work_order": work_order,
        "card_list": card_list,
    }
    html = render_to_string("techdata/widgets/transfer_card_list_table.html", context)
    return html

@dajaxice_register
def removeTransferCard(request, iid):
    """
    JunHU
    """
    print iid
    card = TransferCard.objects.get(id = iid)
    card.delete()

@dajaxice_register
def saveProcessRequirement(request, id, content):
    """
    JunHU
    """
    process = Processing.objects.get(id = id)
    process.technical_requirement = content
    process.save()

@dajaxice_register
def saveAuxiliaryMaterielInfo(request, iid,categories,auxiliary_material_form):
    """
    MH Chen
    """
    materiel = Materiel.objects.get(id = iid)
    material = materiel.material
    material.categories = categories
    material.save()
    auxiliary_material_form = MaterielForm(deserialize_form(auxiliary_material_form),instance = materiel)
    
    if auxiliary_material_form.is_valid():
        auxiliary_material_form.save()
        return  "ok"
    else:
        return "fail"

@dajaxice_register
def getExcuteList(request):
    """
    JunHU
    """
    execute_list = MaterielExecute.objects.filter(is_save = True)
    for execute in execute_list:
        execute.program_list = Program.objects.filter(execute = execute)
    context = {
        "execute_list": execute_list,
    }
    html = render_to_string("techdata/widgets/programme_edit_table.html", context)
    return html

@dajaxice_register
def removeProgram(request, pid):
    """
    JunHU
    """
    try:
        program = Program.objects.get(id = pid)
        program.delete()
        return simplejson.dumps({"ret": True})
    except:
        return simplejson.dumps({"ret": False})

@dajaxice_register
def saveProgramFeedback(request, iid, form):
    """
    JunHU
    """
    execute = MaterielExecute.objects.get(id = iid)
    form = ProgramFeedbackForm(deserialize_form(form))
    if form.is_valid():
        need_correct = form.cleaned_data["need_correct"]
        feedback = form.cleaned_data["feedback"]
        execute.is_save = (not need_correct)
        execute.tech_feedback = feedback
        execute.save()
        return simplejson.dumps({"ret": True, })
    else:
        return simplejson.dumps({"ret": False, })

@dajaxice_register
def getHeatTreatMaterielList(request):
    """
    JunHU
    """
    item_list = HeatTreatmentMateriel.objects.filter(card_belong = None);
    context = {
        "item_list": item_list,
    }
    html = render_to_string("techdata/widgets/tech_hot_deel_table1.html", context)
    return html

@dajaxice_register
def getHeatTreatCardList(request):
    """
    JunHU
    """
    card_list = HeatTreatmentTechCard.objects.all()
    context = {
        "card_list": card_list,
    }
    html = render_to_string("techdata/widgets/tech_hot_deel_table2.html", context)
    return html

@dajaxice_register
def deleteHeatTreatCard(request, card_id):
    """
    JunHU
    """
    card = HeatTreatmentTechCard.objects.get(id = card_id)
    for item in HeatTreatmentMateriel.objects.filter(card_belong = card):
        item.card_belong = None
        item.save()
    card.delete()

@dajaxice_register
def createNewHeatTreatCard(request, selected_item):
    """
    JunHU
    """
    if not selected_item: 
        return
    card = HeatTreatmentTechCard()
    card.save()
    HeatTreatmentArrangement(card_belong = card).save()
    for item_id in selected_item:
        if not item_id: continue
        item = HeatTreatmentMateriel.objects.get(id = item_id)
        item.card_belong = card
        item.save()

@dajaxice_register
def getHeatTreatCardDetail(request, card_id):
    """
    JunHU
    """
    card = HeatTreatmentTechCard.objects.get(id = card_id)
    context = {
        "card": card,
        "STATIC_URL": settings.STATIC_URL,
        "MARK_WRITE": MARK_WRITE,
        "MARK_REVIEW": MARK_REVIEW,
        "HEATTREATMENTCARD_ATTR_TEM_START": HEATTREATMENTCARD_ATTR_TEM_START,
        "HEATTREATMENTCARD_ATTR_TEM_END": HEATTREATMENTCARD_ATTR_TEM_END,
        "HEATTREATMENTCARD_ATTR_TEM_TOP": HEATTREATMENTCARD_ATTR_TEM_TOP,
        "HEATTREATMENTCARD_ATTR_TEM_UP_SPEED": HEATTREATMENTCARD_ATTR_TEM_UP_SPEED,
        "HEATTREATMENTCARD_ATTR_TEM_DOWN_SPEED": HEATTREATMENTCARD_ATTR_TEM_DOWN_SPEED,
        "HEATTREATMENTCARD_ATTR_TEM_TIME": HEATTREATMENTCARD_ATTR_TEM_TIME,
    }
    html = render_to_string("techdata/widgets/heat_treatment_tech_card.html", context)
    return html

@dajaxice_register
def heatTreatCardVariableSave(request, card_id, attr, content):
    """
    JunHU
    """
    card = HeatTreatmentTechCard.objects.get(id = card_id)
    setattr(card, attr, content)
    card.save()

@dajaxice_register
def heatTreatCardMark(request, card_id, step):
    """
    JunHU
    """
    card = HeatTreatmentTechCard.objects.get(id = card_id)
    if step == MARK_WRITE:
        card.writer = request.user
        card.write_date = datetime.datetime.today()
        card.file_index = "%06d" % (card.id) # 暂定
        card.save()
        context = {
            "ret": True,
            "mark_user": unicode(card.writer.userinfo),
            "file_index": card.file_index,
        }
    elif step == MARK_REVIEW:
        if card.writer == None:
            context = {
                "ret": False,
                "warning": u"工艺卡还未完成编制",
            }
            return simplejson.dumps(context)
        card.reviewer = request.user
        card.review_date = datetime.datetime.today()
        card.save()
        context = {
            "ret": True,
            "mark_user": unicode(card.reviewer.userinfo),
        }
    else:
        context = {
            "ret": False,
            "warning": u"后台保存错误"
        }
    return simplejson.dumps(context)

@dajaxice_register
def designBOMWriterConfirm(request, id_work_order):
    """
    mxl
    """
    order = WorkOrder.objects.get(id = id_work_order)
    if DesignBOMMark.objects.filter(order = order).count() == 0:
        DesignBOMMark(order = order).save()
    order.designbommark.writer = request.user
    order.designbommark.write_date = datetime.datetime.today()
    order.designbommark.save()
    return simplejson.dumps({"ret" : True, "user" : unicode(request.user.userinfo)})


@dajaxice_register
def designBOMReviewerConfirm(request, id_work_order):
    """
    mxl
    """
    order = WorkOrder.objects.get(id = id_work_order)
    if DesignBOMMark.objects.filter(order = order).count() == 0:
        DesignBOMMark(order = order).save()

    if order.designbommark.writer == None:
        return simplejson.dumps({"ret": False})
    order.designbommark.reviewer = request.user
    order.designbommark.review_date = datetime.datetime.today()
    order.designbommark.save()
    return simplejson.dumps({"ret": True, "user": unicode(request.user.userinfo)})

@dajaxice_register
def getTechPreparationPlan(request, id_work_order, month, year):
    """
    mxl
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    tech_plan = TechPlan.objects.filter(order = work_order).filter(month = month).filter(year = year)
    context = {
        "work_order" : work_order,
        "tech_plan" : tech_plan,
    }
    html = render_to_string("techdata/widgets/tech_preparation_plan_table.html", context)
    return html

@dajaxice_register
def getTechPlanForm(request, iid):
    """
    mxl
    """
    if iid == -1:
        form = TechPreparationPlanForm()
    else:
        techplan = TechPlan.objects.get(id = iid)
        form = TechPreparationPlanForm(instance = techplan)
    form_html = render_to_string("techdata/widgets/tech_preparation_plan_form.html", {"form" : form})
    return form_html

@dajaxice_register
def saveTechPlan(request, id_work_order, tech_preparation_plan_form, addOrUpdate, iid):
    """
    mxl
    """
    if addOrUpdate == "add":
        tech_preparation_plan_form =  TechPreparationPlanForm(deserialize_form(tech_preparation_plan_form))    
        order = WorkOrder.objects.get(id = id_work_order)
        if tech_preparation_plan_form.is_valid():
            techplan = tech_preparation_plan_form.save(commit=False)
            techplan.order = order
            curDate = datetime.datetime.today()
            techplan.month = curDate.month
            techplan.year = curDate.year
            techplan.save()
            return simplejson.dumps({"ret" : "ok"})
        else:
            for f in tech_preparation_plan_form.fields:
                if tech_preparation_plan_form[f].errors:
                    print tech_preparation_plan_form[f]
    else:
        techplan = TechPlan.objects.get(id = iid)
        tech_preparation_plan_form =  TechPreparationPlanForm(deserialize_form(tech_preparation_plan_form), instance = techplan)
        if tech_preparation_plan_form.is_valid():
            tech_preparation_plan_form.save()
            return simplejson.dumps({"ret" : "ok"}) 
    form_html = render_to_string("techdata/widgets/tech_preparation_plan_form.html", {"form" : tech_preparation_plan_form})
    return simplejson.dumps({"ret" : "false", "form_html" : form_html})

@dajaxice_register
def getHeatPointDetail(request, card_id):
    """
    BinWu
    """
    upload = UploadForm()
    card = HeatTreatmentTechCard.objects.get(id = card_id)
    context = {
        "card": card,
        "upload" : upload,
        "STATIC_URL": settings.STATIC_URL,
        "MARK_WRITE": MARK_WRITE,
        "MARK_REVIEW": MARK_REVIEW,
        "HEATTREATMENTCARD_ATTR_TEM_START": HEATTREATMENTCARD_ATTR_TEM_START,
        "HEATTREATMENTCARD_ATTR_TEM_END": HEATTREATMENTCARD_ATTR_TEM_END,
        "HEATTREATMENTCARD_ATTR_TEM_TOP": HEATTREATMENTCARD_ATTR_TEM_TOP,
        "HEATTREATMENTCARD_ATTR_TEM_UP_SPEED": HEATTREATMENTCARD_ATTR_TEM_UP_SPEED,
        "HEATTREATMENTCARD_ATTR_TEM_DOWN_SPEED": HEATTREATMENTCARD_ATTR_TEM_DOWN_SPEED,
        "HEATTREATMENTCARD_ATTR_TEM_TIME": HEATTREATMENTCARD_ATTR_TEM_TIME,
    }
    html = render_to_string("techdata/widgets/heat_point_graph.html", context)
    return html

@dajaxice_register
def heatTreatmentArrangementWrite(request, card_id):
    """
    BinWu
    """
    card = HeatTreatmentTechCard.objects.get(id = card_id)
    if HeatTreatmentArrangement.objects.filter(card_belong = card).count() == 0:
        return simplejson.dumps({"res" : False})
    card.heattreatmentarrangement.writer = request.user
    card.heattreatmentarrangement.file_index = "%06d" % (card.heattreatmentarrangement.id)
    card.heattreatmentarrangement.write_date = datetime.datetime.today()
    card.heattreatmentarrangement.save()
    context = {
        "res" : True,
        "writer" : unicode(request.user.userinfo),
        "bianhao" : card.heattreatmentarrangement.file_index,
    }
    return simplejson.dumps(context)

@dajaxice_register 
def heatTreatmentArrangementReview(request, card_id):
    """
    BinWu
    """
    card = HeatTreatmentTechCard.objects.get(id = card_id)
    if HeatTreatmentArrangement.objects.filter(card_belong = card).count() == 0 or not card.heattreatmentarrangement.writer:
        return simplejson.dumps({"res" : False, })
    else:
        card.heattreatmentarrangement.reviewer = request.user
        card.heattreatmentarrangement.review_date = datetime.datetime.today()
        card.heattreatmentarrangement.save()
        return simplejson.dumps({"res" : True, "reviewer" : unicode(request.user.userinfo)})

@dajaxice_register
def weldQuotaWriterConfirm(request, id_work_order):
    """
    MH Chen
    """
    order = WorkOrder.objects.get(id = id_work_order)
    if WeldQuotaPageMark.objects.filter(order = order).count() == 0:
        WeldQuotaPageMark(order = order).save()
    order.weldquotapagemark.writer = request.user
    order.weldquotapagemark.write_date = datetime.datetime.today()
    order.weldquotapagemark.save()
    return simplejson.dumps({"ret": True, "user": unicode(request.user.userinfo)})

@dajaxice_register
def weldQuotaReviewerConfirm(request, id_work_order):
    """
    MH Chen
    """
    order = WorkOrder.objects.get(id = id_work_order)
    if WeldQuotaPageMark.objects.filter(order = order).count() == 0:
        WeldQuotaPageMark(order = order).save()
    
    if order.weldquotapagemark.writer == None:
        return simplejson.dumps({"ret": False})
    order.weldquotapagemark.reviewer = request.user
    order.weldquotapagemark.reviewe_date = datetime.datetime.today()
    order.weldquotapagemark.save()
    return simplejson.dumps({"ret": True, "user": unicode(request.user.userinfo)})

@dajaxice_register
def getInstallWeldList(request):
    """
    JunHU
    """
    orders = WorkOrder.objects.all()
    context = {
        "orders": orders,
    }
    html = render_to_string("techdata/widgets/tech_install_weld_table.html", context)
    return html

@dajaxice_register
def getTechInstallWeldCard(request, iid):
    """
    JunHU
    """
    order = WorkOrder.objects.get(id = iid)
    context = {
        "order": order,
    }
    html = render_to_string("techdata/widgets/tech_install_weld_card.html", context)
    return html


@dajaxice_register
def getWorkOrderOfConnectList(request):
    """
    mxl
    """
    work_order_list = WorkOrder.objects.all()
    for work_order in work_order_list:
        work_order.connectOrientation_list = ConnectOrientation.objects.filter(order = work_order)
    context = {
        "work_order_list": work_order_list,
    }
    html = render_to_string("techdata/widgets/connection_orientation_edit_table.html", context)
    return html

@dajaxice_register
def removeConnectOrientation(request, pid):
    """
    JunHU
    """
    try:
        connect = ConnectOrientation.objects.get(id = pid)
        connect.delete()
        return simplejson.dumps({"ret": True})
    except:
        return simplejson.dumps({"ret": False})


def validateWeldSeams(jointArray):
    if len(jointArray) == 0:
        return None
    fields = ['weld_method_1', 'weld_method_2', 'base_metal_1', 'base_metal_2', 'base_metal_thin_1', 'base_metal_thin_2']
    weldseam = WeldSeam.objects.get(id = jointArray[0])
    joint_index_list = []
    joint_index_list.append(weldseam.weld_index)
    for i in range(1, len(jointArray)):
        seam_id = jointArray[i]
        seam = WeldSeam.objects.get(id = seam_id)
        joint_index_list.append(seam.weld_index)
        for field in fields:
            if getattr(weldseam, field) != getattr(seam, field):
                return None
    return weldseam, ','.join(joint_index_list)


@dajaxice_register
def getWeldJointDetailForm(request, jointArray):
    weldseam, joint_index = validateWeldSeams(jointArray)
    if weldseam == None:
        return simplejson.dumps({"ret" : "err"})
    else:
        fields = ['base_metal_1', 'base_metal_2', 'base_metal_thin_1', 'base_metal_thin_2', "weld_position"]
        map = {
            'base_metal_1' : 'bm_texture_1', 
            'base_metal_2' : 'bm_texture_2', 
            'base_metal_thin_1' : 'bm_specification_1', 
            'base_metal_thin_2' : 'bm_specification_2',
            "weld_position": "weld_position",
        }
        print weldseam.weld_position
        data = {}
        for field in fields:
            data[map[field]] = getattr(weldseam, field)
        data['joint_index'] = joint_index
        weld_joint_detail_form = WeldJointTechDetailForm(data)
#        weld_joint_detail_form.fields["weld_certification_1"].queryset = WeldCertification.objects.filter(weld_method = weldseam.weld_method_1)
#        weld_joint_detail_form.fields["weld_certification_2"].queryset = WeldCertification.objects.filter(weld_method = weldseam.weld_method_2)
        context = {
            "form" : weld_joint_detail_form,
        }
        html = render_to_string("techdata/widgets/weldjoint_detail.html", context)
        return simplejson.dumps({"ret" : "ok", "html" : html, "weld_method_1" : weldseam.weld_method_1.id if weldseam.weld_method_1 else -1, "weld_method_2" : weldseam.weld_method_2.id if weldseam.weld_method_2 else -1})

@dajaxice_register
def saveJointDetail(request, weld_joint_detail_form, jointArray, id_work_order):
    """
    mxl
    """
    weld_joint_detail_form = WeldJointTechDetailForm(deserialize_form(weld_joint_detail_form))
    if weld_joint_detail_form.is_valid():
        weld_joint_detail = weld_joint_detail_form.save(commit = False)
        weld_joint_detail.specification = WeldingProcessSpecification.objects.get(order__id = id_work_order)
        weld_joint_detail.save()

        wwi = WeldingWorkInstruction(detail = weld_joint_detail)
        wwi.file_index = WeldingWorkInstruction.objects.filter(detail__specification__order = weld_joint_detail.specification.order).count() + 1
        wwi.save()
    else:
        context = {
            "form" : weld_joint_detail_form
        }
        html = render_to_string("techdata/widgets/weldjoint_detail.html", context)
        return simplejson.dumps({"ret" : "err", "html" : html})
    for seam_id in jointArray:
        seam = WeldSeam.objects.get(id = seam_id)
        seam.weld_joint_detail = weld_joint_detail
        seam.save()
    return simplejson.dumps({"ret" : "ok"})


#@dajaxice_register
#def saveWeldJointIndex(request, id_work_order, index):
#    weld_joint = WeldJointTech.objects.get(order__id = id_work_order)
#    weld_joint.index = index
#    weld_joint.save()
#    return "ok"
#
#@dajaxice_register
#def deleteWeldJointDetail(request, uid):
#    weld_joint_detail = WeldJointTechDetail.objects.get(id = uid)
#    weld_joint_detail.delete()
#    return "ok"



@dajaxice_register
def getWeldingProcessSpecification(request, id_work_order, page = "1", is_print = False):
    """
    JunHU
    """
    work_order = WorkOrder.objects.get(id = id_work_order)

    work_order.schematic_index = Materiel.objects.get(Q(order = work_order) & Q(index = "1")).schematic_index
    specification = WeldingProcessSpecification.objects.get(order = work_order)
    page = int(page)

    detail_list = WeldJointTechDetail.objects.filter(Q(specification = specification))
    
    detail_list_page = 1 if detail_list.count() == 0 else (detail_list.count() - 1) / 6 + 1

    total_page = 2 + detail_list_page + 2

    context = {
        "work_order": work_order,
        "specification": specification,
        "current_page": page,
        "total_page": total_page,
        "is_print": is_print,
    }
    context["display_current_page"] = context["current_page"] - 1
    context["display_total_page"] = context["total_page"] - 1

    if page == 1:
        html = render_to_string("techdata/welding_process_specification/cover.html", context)
    elif page == 2:
        html = render_to_string("techdata/welding_process_specification/graph_page.html", context)
    elif page <= 2 + detail_list_page:
        detail_list = getContext(detail_list, page - 2, "item", 1, 6)["item_list"]
        context["detail_list"] = detail_list
        context["empty_row"] = range(6 - len(detail_list))
        html = render_to_string("techdata/welding_process_specification/weld_analysis_table.html", context)
    elif page <= 2 + detail_list_page + 1:
        html = render_to_string("techdata/welding_process_specification/welding_material_summary.html", context)
    else:
        context["empty_row"] = range(11)
        html = render_to_string("techdata/welding_process_specification/NDE.html", context)
    return html

@dajaxice_register
def getCard(request):
    """
    MH Chen
    """
    context = {"STATIC_URL": settings.STATIC_URL,}
    html = render_to_string("techdata/widgets/weld_instruction_book.html",context)
    return html
