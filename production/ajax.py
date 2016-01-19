#!/usr/bin/env python
# coding=utf-8

from dajax.core import Dajax
from django.template.loader import render_to_string
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from const.models import WorkOrder
from production.models import SynthesizeFileListStatus

@dajaxice_register
def getFileList(request, id_work_order):
    """
    Lei
    """
    workorder = SynthesizeFileListStatus.objects.filter(workorder_id__id = id_work_order)
    context = {
        "workorder":workorder,
    }
    html = render_to_string("production/synthesize_detail_filelist.html",context)
    return html

@dajaxice_register
def changeFileList(request, id, workorder_id):
    """
    Lei
    """
    workorder = SynthesizeFileListStatus.objects.filter(workorder_id__order_index = workorder_id)[0]
    exec("workorder.%s=True"%id)
    workorder.save()
    context = {
        "workorder":[workorder],
    }
    html = render_to_string("production/synthesize_detail_filelist.html",context)
    return html