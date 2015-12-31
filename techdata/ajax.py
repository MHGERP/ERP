#!/usr/bin/env python
# coding=utf-8

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.utils import simplejson

from django.db.models import Q
from django.contrib.auth.models import User

from backend.utility import getContext
from const.models import *
from forms import MaterielForm

from techdata.forms import *
from techdata.models import *
from const.models import *
from const.utils import getMaterialQuerySet

@dajaxice_register
def getProcessBOM(request, id_work_order):
    """
    JunHU
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    BOM = Materiel.objects.filter(order = work_order)
    for item in BOM:
        if CirculationRoute.objects.filter(materiel_belong = item).count() == 0:
            CirculationRoute(materiel_belong = item).save()
        item.route = '.'.join(getattr(item.circulationroute, "L%d" % i).name for i in xrange(1, 11) if getattr(item.circulationroute, "L%d" % i))
    context = {
        "work_order": work_order,
        "BOM": BOM,
    }
    html = render_to_string("techdata/widgets/processBOM_table.html", context)
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
def getDesignBOM(request, id_work_order):
    """
    mxl
    """
    work_order = WorkOrder.objects.get(id = id_work_order)
    BOM = Materiel.objects.filter(order = work_order)
    for item in BOM:
        if CirculationRoute.objects.filter(materiel_belong = item).count() == 0:
            CirculationRoute(materiel_belong = item).save()
        item.route = '.'.join(getattr(item.circulationroute, "L%d" % i).name for i in xrange(1, 11) if getattr(item.circulationroute, "L%d" % i))
    context = {
        "work_order" : work_order,
        "BOM" : BOM,
    }
    html = render_to_string("techdata/widgets/designBOM_table.html", context)
    return html

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
def getWeldSeamCard(self):
    """
    JunHU
    """
    form = WeldSeamForm()
    material_set = getMaterialQuerySet(WELD_ROD, WELD_WIRE, WELD_RIBBON, WELD_FLUX)
    form.fields["weld_material_1"].queryset = material_set
    form.fields["weld_material_2"].queryset = material_set
    context = {
        "form": form,
    }
    html = render_to_string("techdata/widgets/weld_seam_card.html", context)
    return html

@dajaxice_register
def boxOutBought(request):
    """
    BinWu
    """
    list = Materiel.objects.all();
    context = {
        "list" : list,
    }
    html = render_to_string("techdata/widgets/tech_box_outbought_table.html", context)
    return html

@dajaxice_register
def firstFeeding(request):
    """
    BinWu
    """
    list = Materiel.objects.all();
    context = {
        "list" : list,
    }
    html = render_to_string("techdata/widgets/first_feeding_table.html", context)
    return html

@dajaxice_register
def principalMaterial(request):
    """
    BinWu
    """
    list = Materiel.objects.all();
    context = {
        "list" : list,
    }
    html = render_to_string("techdata/widgets/principal_material_table.html", context)
    return html

@dajaxice_register
def auxiliaryMaterial(request):
    """
    BinWu
    """
    list = Materiel.objects.all();
    context = {
        "list" : list,
    }
    html = render_to_string("techdata/widgets/auxiliary_material_table.html", context)
    return html

@dajaxice_register
def weldList(request):
    """
    BinWu
    """
    list = Materiel.objects.all();
    context = {
        "list" : list,
    }
    html = render_to_string("techdata/widgets/weld_list_table.html", context)
    return html

@dajaxice_register
def techBoxWeld(request):
    """
    BinWu
    """
    list = Materiel.objects.all();
    context = {
        "list" : list,
    }
    html = render_to_string("techdata/widgets/tech_box_weld_table.html", context)
    return html

@dajaxice_register
def weldQuota(request):
    """
    BinWu
    """
    list = Materiel.objects.all();
    context = {
        "list" : list,
    }
    html = render_to_string("techdata/widgets/weld_quota_table.html", context)
    return html

@dajaxice_register
def addWeldSeam(request, iid, form):
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
        
