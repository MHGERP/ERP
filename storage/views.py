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

from models import *

def weldMaterialHomeViews(request):
    context = {
        
    }
    print "hahsd"
    return render(request,"storage/weldmaterial/weldmaterialhome.html",context)

def Weld_Apply_Card_List(request):
    context={}
    weld_apply_cards=WeldingMaterialApplyCard.objects.all().order_by('create_time')#考虑效率问题，注意更改all的获取方式
    context['weld_apply_cards']=weld_apply_cards
    context['departments']=['部门1','部门2','部门3','部门4']
    return render(request,'storage/weldapply/weldapplycardlist.html',context)

def Weld_Apply_Card_Detail(request):
    context={}
    card_index=10086 #request.GET['apply_card_index']
    apply_card=WeldingMaterialApplyCard.objects.get(index=card_index)
    context['apply_card']=apply_card
    return render(request,'storage/weldapply/weldapplycarddetail.html',context)
