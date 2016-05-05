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
from backend.utility import getContext
from const.models import *
from forms import MaterielForm

from techdata.forms import *
from techdata.models import *
from const.models import *
from const.utils import getMaterialQuerySet

from purchasing.models import MaterielExecute, MaterielExecuteDetail
import datetime

@dajaxice_register
def getProcessBOM(request, id_work_order):
    """
    JunHU
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    BOM = Materiel.objects.filter(order = work_order)
    for item in BOM:
        item.route = ' '.join(getattr(item.circulationroute, "L%d" % i).get_name_display() for i in xrange(1, 11) if getattr(item.circulationroute, "L%d" % i))   
        if item.net_weight and item.count:
            item.total_weight = item.net_weight * int(item.count)
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
    if CirculationRoute.objects.filter(materiel_belong = item).count() == 0:
        CirculationRoute(materiel_belong = item).save()
    item.route = ' '.join(getattr(item.circulationroute, "L%d" % i).get_name_display() for i in xrange(1, 11) if getattr(item.circulationroute, "L%d" % i))     
    if item.net_weight and item.count:
        item.total_weight = item.net_weight * int(item.count)   
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
def getDesignBOM(request, id_work_order):
    """
    mxl
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    BOM = Materiel.objects.filter(order = work_order)
    for item in BOM:
        if CirculationRoute.objects.filter(materiel_belong = item).count() == 0:
            CirculationRoute(materiel_belong = item).save()
        item.route = '.'.join(getattr(item.circulationroute, "L%d" % i).get_name_display() for i in xrange(1, 11) if getattr(item.circulationroute, "L%d" % i))
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
    if CirculationRoute.objects.filter(materiel_belong = item).count() == 0:
        circulationroute(materiel_belong = item).save()
    item.route = '.'.join(getattr(item.circulationroute, "L%d" % i).get_name_display() for i in xrange(1, 11) if getattr(item.circulationroute, "L%d" % i))
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
def getWeldSeamCard(self, full = False, iid = None):
    """
    JunHU
    """
    if iid:
        weld_seam = WeldSeam.objects.get(id = iid)
        form = WeldSeamForm(instance = weld_seam)
    else:
        form = WeldSeamForm()
    material_set = getMaterialQuerySet(WELD_ROD, WELD_WIRE, WELD_RIBBON, WELD_FLUX)
    form.fields["weld_material_1"].queryset = material_set
    form.fields["weld_material_2"].queryset = material_set
    context = {
        "form": form,
    }
    if full:
        html = render_to_string("techdata/widgets/weld_seam_full_card.html", context)
    else:
        html = render_to_string("techdata/widgets/weld_seam_card.html", context)
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
def weldQuota(request, order):
    """
    MH Chen
    """
    list = Materiel.objects.filter(order = order)
    context = {
        "list" : list,
    }
    html = render_to_string("techdata/widgets/weld_quota_table.html", context)
    return html

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
def getWeldSeamList(self, id_work_order):
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

    return simplejson.dumps({"html": html, "read_only": read_only})

@dajaxice_register
def getWeldSeamWeight(self, id_work_order):
    """
    MH Chen
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    weldseam_list = WeldSeam.objects.filter(materiel_belong__order = work_order)
    dic = {}

    # items = WeldSeam.objects.values('weld_material_1__categories', 'size_1',"weld_material_2__categories","size_1").annotate(Sum('hour'))

    for item1 in weldseam_list:
        if dic.has_key((item1.weld_material_1,item1.size_1,item1.weld_material_1.categories)):
            dic[(item1.weld_material_1,item1.size_1,item1.weld_material_1.categories)]+= int(item1.weight_1)
        else:
            dic[(item1.weld_material_1,item1.size_1,item1.weld_material_1.categories)] = int(item1.weight_1)
    for item2 in weldseam_list:
        if item2.weld_material_2 != None:
            if dic.has_key((item2.weld_material_2,item2.size_2,item2.weld_material_2.categories)):
                dic[(item2.weld_material_2,item2.size_2,item2.weld_material_2.categories)]+= int(item2.weight_2)
            else:
                dic[(item2.weld_material_2,item2.size_2,item2.weld_material_2.categories)] = int(item2.weight_2)

    context = {
        "work_order":work_order,
        "dic":dic,
    }
    html = render_to_string("techdata/widgets/weld_quota_table.html", context)
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
def getSingleWeldSeamInfo(self, iid):
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
def getTransferCard(request, iid, card_type = None):
    """
    JunHU
    """
    item = Materiel.objects.get(id = iid)
    if CirculationRoute.objects.filter(materiel_belong = item).count() == 0:
        CirculationRoute(materiel_belong = item).save()
    item.route = '.'.join(getattr(item.circulationroute, "L%d" % i).get_name_display() for i in xrange(1, 11) if getattr(item.circulationroute, "L%d" % i))     
    
    try:
        process = Processing.objects.get(materiel_belong = item, is_first_processing = True)  
        process_list = []
        while process:
            process_list.append(process)
            process = process.next_processing
    except:
        process_list = []
    
    context = {
        "item": item,
        "process_list": process_list,
        "MARK_WRITE": MARK_WRITE,
        "MARK_REVIEW": MARK_REVIEW,
        "MARK_PROOFREAD": MARK_PROOFREAD,
        "MARK_APPROVE": MARK_APPROVE,
    }

    cards = TransferCard.objects.filter(materiel_belong = item)
    if cards:
        context["card"] = cards[0]
        html = render_to_string(CARD_TYPE_TO_HTML[cards[0].card_type], context)
    else:
        html = render_to_string(CARD_TYPE_TO_HTML[card_type], context)
    return html

@dajaxice_register
def transferCardMark(request, iid, step, card_type = None):
    """
    JunHU
    """
    def date2str(date):
        return str(date.year) + "." + "%02d" % date.month + "." + str(date.day)
    
    item = Materiel.objects.get(id = iid)
    context = {}
    if step == MARK_WRITE:
        if TransferCard.objects.filter(materiel_belong = item).count() > 0:
            context = {
                "ret": False,
                "warning": u"已为该零件创建流转卡",
            }
            return simplejson.dumps(context)

        card = TransferCard(materiel_belong = item, card_type = card_type)
        card.save()
        card.file_index = "%06d" % (card.id)
        card.save()
        mark = TransferCardMark(card = card)
        mark.save()
        card.transfercardmark.writer = request.user
        card.transfercardmark.write_date = datetime.datetime.today()
        card.transfercardmark.save()
        context = {
            "ret": True,
            "file_index": unicode(card),
            "mark_user": unicode(card.transfercardmark.writer.userinfo),
            "mark_date": date2str(card.transfercardmark.write_date)
        }
        print context
    elif step == MARK_PROOFREAD:
        cards = TransferCard.objects.filter(materiel_belong = item)
        if cards.count() == 0 or cards[0].transfercardmark.writer == None:
            context = {
                "ret": False,
                "warning": u"该流转卡还未完成编制",
            }
            return simplejson.dumps(context)

        card = cards[0]
        card.transfercardmark.proofreader = request.user
        card.transfercardmark.proofread_date = datetime.datetime.today()
        card.transfercardmark.save()
        context = {
            "ret": True,
            "mark_user": unicode(card.transfercardmark.proofreader.userinfo),
            "mark_date": date2str(card.transfercardmark.proofread_date)
        }
    elif step == MARK_REVIEW:
        cards = TransferCard.objects.filter(materiel_belong = item)
        if cards.count() == 0 or cards[0].transfercardmark.proofreader == None:
            context = {
                "ret": False,
                "warning": u"该流转卡还未完成校对",
            }
            return simplejson.dumps(context)

        card = cards[0]
        card.transfercardmark.reviewer = request.user
        card.transfercardmark.review_date = datetime.datetime.today()
        card.transfercardmark.save()
        context = {
            "ret": True,
            "mark_user": unicode(card.transfercardmark.reviewer.userinfo),
            "mark_date": date2str(card.transfercardmark.review_date)
        }
    elif step == MARK_APPROVE:
        cards = TransferCard.objects.filter(materiel_belong = item)
        if cards.count() == 0 or cards[0].transfercardmark.reviewer == None:
            context = {
                "ret": False,
                "warning": u"该流转卡还未完成审核",
            }
            return simplejson.dumps(context)

        card = cards[0]
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

@dajaxice_register
def getWeldJointDetailForm(request, weld_method, bm_specification_1, bm_specification_2, iid = None):
    if iid:
        weld_joint_detail = WeldJointTechDetail.objects.get(id = iid)
        weld_joint_detail_form = WeldJointTechDetailForm(instance = weld_joint_detail)
    else:
        weld_joint_detail_form = WeldJointTechDetailForm()
        weld_joint_detail_form.fields["weld_method"] = weld_method
        weld_joint_detail_form.fields["bm_specification_1"] = bm_specification_1
        weld_joint_detail_form.fields["bm_specification_2"] = bm_specification_2
    context = {
        "form" : weld_joint_detail_form
    }
    return render_to_string("techdata/widgets/weldjoint_detail.html", context)


#@dajaxice_register
#def addToJointDetail(request, id_work_order, jointArray):
#    """
#    mxl
#    """
#    workorder = WorkOrder.objects.get(id = id_work_order)
#    if WeldJointTech.objects.filter(order = workorder).count == 0:
#        weld_joint = WeldJointTech(order = workorder).save()
#    else:
#        weld_joint = WeldJointTech.objects.filter(order = workorder)[0]
#    weld_joint_detail = WeldJointTechDetail(weld_joint = weld_joint)
#    for id in jointArray:
#        weldseam = WeldSeam.objects.get(id = id)
#        weld_joint_detail.specification = weldseam
#           

