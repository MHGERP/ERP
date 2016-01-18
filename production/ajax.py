#!/usr/bin/env python
# coding=utf-8

from dajax.core import Dajax
from django.template.loader import render_to_string
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from const.models import WorkOrder

@dajaxice_register
def getFileList(request, id_work_order):
	"""
	Lei
	"""
	workorder = WorkOrder.objects.get(id = id_work_order)
	print workorder.order_index
	context = {
	    "workorder":workorder,
	}
	html = render_to_string("production/synthesize_detail_filelist.html",context)
	return html