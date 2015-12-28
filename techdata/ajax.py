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
