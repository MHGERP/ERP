# coding: UTF-8
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
import json, datetime
from django.db import transaction
from django.contrib.auth.models import User
from backend.utility import getContext
from sell.models import *
from users.models import Group

def productionsView(request):
    context = {

    }
    return render(request, "sell/productions.html", context)

def product_bidFile_add(request):
    if request.is_ajax():
        if request.FILES['product_file'].size > 10 * 1024 * 1024:
            file_upload_error = 2
        else:
            product_id = request.POST['product_id']
            group_type = request.POST['group_type']
            #print product_id
            #print group_type
            product = Product.objects.get(id = product_id)
            bidfile = BidFile()
            bidfile.file_obj = request.FILES['product_file']
            bidfile.file_size = str(int(request.FILES['product_file'].size) / 1000) + "kb"
            bidfile.name = request.FILES['product_file'].name
            bidfile.upload_date = datetime.datetime.now()
            bidfile.save()
            if group_type == "manufacture":
                group = Group.objects.filter(name__icontains = u"生产")
                product.manufacture_file_down = bidfile
            elif group_type == "techdata":
                group = Group.objects.filter(name__icontains = u"工艺")
                product.techdata_file_down = bidfile
            else:
                group = Group.objects.filter(name__icontains = u"采购")
                product.purchasing_file_down = bidfile
            bidfile.recv_group = group[0] if len(group) > 0 else None
            bidfile.save()
            product.save()
            file_upload_error = 1
        return HttpResponse(json.dumps({"file_upload_error" : file_upload_error, }))


def product_bidFile_back(request):
    if request.is_ajax():
        if request.FILES['product_file'].size > 10 * 1024 * 1024:
            file_upload_error = 2
        else:
            print "back"
            product_id = request.POST['product_id']
            group_type = request.POST['group_type']
            #print product_id
            #print group_type
            product = Product.objects.get(id = product_id)
            bidfile = BidFile(file_type = True)
            bidfile.file_obj = request.FILES['product_file']
            bidfile.file_size = str(int(request.FILES['product_file'].size) / 1000) + "kb"
            bidfile.name = request.FILES['product_file'].name
            bidfile.upload_date = datetime.datetime.now()
            bidfile.save()
            if group_type == "manufacture":
                group = Group.objects.filter(name__icontains = u"生产")
                product.manufacture_file_up = bidfile
            elif group_type == "techdata":
                group = Group.objects.filter(name__icontains = u"工艺")
                product.techdata_file_up = bidfile
            else:
                group = Group.objects.filter(name__icontains = u"采购")
                product.purchasing_file_up = bidfile
            bidfile.recv_group = group[0] if len(group) > 0 else None
            bidfile.save()
            product.save()
            file_upload_error = 1
        return HttpResponse(json.dumps({"file_upload_error" : file_upload_error, }))

def bidFile_to_manufacture(request):
    context = {

    }
    return render(request, "sell/bidFile_to_manufacture.html", context)

def bidFile_to_techdata(request):
    context = {
        
    }
    return render(request, "sell/bidFile_to_techdata.html", context)

def bidFile_to_purchasing(request):
    context = {
        
    }
    return render(request, "sell/bidFile_to_purchasing.html", context)

def productions_audit(request):
    context = {
        
    }
    return render(request, "sell/product_audit.html", context)
