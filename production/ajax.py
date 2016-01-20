#!/usr/bin/env python
# coding=utf-8

from dajax.core import Dajax
from django.template.loader import render_to_string
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from const.models import WorkOrder,Materiel
from production.models import SynthesizeFileListStatus
from techdata.models import Processing

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

@dajaxice_register
def getHourSummarize(request, id_work_order, work_ticket, group_num):
    """
    Lei
    """
    if work_ticket:
        materiel = Materiel.objects.filter(order__order_index=id_work_order,index=work_ticket)
    else:
        materiel = Materiel.objects.filter(order__order_index=id_work_order)
    processSet = []
    for item in materiel:
        if group_num:
            process = Processing.objects.filter(materiel_belong=item,operator__username=group_num);
            processSet.append(process)
        else:
            process = Processing.objects.filter(materiel_belong=item);
            processSet.append(process)
    context = {
        "processSet":processSet
    }
    html = render_to_string("production/man_hour_message_list.html",context)
    return html