# coding:UTF-8

from django.shortcuts import render

from const import *
from const.forms import InventoryTypeForm
from django.http import HttpResponseRedirect
from datetime import datetime
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q

from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
from django.db import transaction

def weldMaterialHomeViews(request):
    context = {
        
    }
    print "hahsd"
    return render(request,"storage/weldmaterial/weldmaterialhome.html",context)
