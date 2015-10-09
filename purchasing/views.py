from django.shortcuts import render
from purchasing.models import BidForm,ArrivalInspection,Supplier,PurchasingEntry,\
    PurchasingEntryItems,SupplierFile,MaterialSubApply,MaterialSubApplyItems
from const import *
from const.forms import InventoryTypeForm
from const.models import WorkOrder, InventoryType
from purchasing.forms import SupplierForm,EntryForm,SubApplyForm,SubApplyItemForm,SubApplyInspectForm
from datetime import datetime
from django.template import RequestContext
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
def purchasingFollowingViews(request):
    """
    chousan1989
    """
    bidform_processing=BidForm.objects.filter(bid_status__main_status__gte=BIDFORM_STATUS_SELECT_SUPPLIER,bid_status__main_status__lte=BIDFORM_STATUS_CHECK_STORE)

    context={
        "bidform":bidform_processing,
        "BIDFORM_STATUS_SELECT_SUPPLIER":BIDFORM_STATUS_SELECT_SUPPLIER,
        "BIDFORM_STATUS_INVITE_BID":BIDFORM_STATUS_INVITE_BID,
        "BIDFORM_STATUS_PROCESS_FOLLOW":BIDFORM_STATUS_PROCESS_FOLLOW,
        "BIDFORM_STATUS_CHECK_STORE":BIDFORM_STATUS_CHECK_STORE 
    }

    return render(request,"purchasing/purchasing_following.html",context)


def pendingOrderViews(request):
    
    """
    JunHU
    summary: view function of pendingorder page
    params: NULL
    return: NULL
    """
    return render(request, "purchasing/pending_order.html")

def materialSummarizeViews(request):
    """
    JunHU
    summary: view function of meterialSummarize page
    params: NULL
    return: NULL
    """
    inventoryTypeForm = InventoryTypeForm()
    context = {"inventoryTypeForm": inventoryTypeForm}
    return render(request, "purchasing/material_summarize.html", context)

def selectSupplierViews(request):
    context={}
    return render(request,"purchasing/select_supplier.html",context)

def supplierManagementViews(request):
    file_upload_error=0
    if request.method=="POST":
        if request.FILES['supplier_file'].size>10*1024*1024:
            file_upload_error=2
        else:
            supplier_id=request.POST['supplier_id']
            supplier=Supplier.objects.get(pk=supplier_id)
            file=SupplierFile()
            file.project=supplier
            file.file_obj=request.FILES['supplier_file']
            file.file_size=str(int(request.FILES['supplier_file'].size)/1000)+"kb"
            file.name=request.FILES['supplier_file'].name
            file.upload_time= datetime.now()
            file.save()
            file_upload_error=1
    suppliers=Supplier.objects.all()
    supplier_form=SupplierForm()
    context={
        "suppliers":suppliers,
        "supplier_form":supplier_form,
        "file_upload_error":file_upload_error
    }
    return render(request,"purchasing/supplier/supplier_management.html",context)
def bidTrackingViews(request):
    context = {}
    return render(request, "purchasing/bid_track.html", context)

@csrf.csrf_protect
def arrivalInspectionViews(request):
    if request.method == "POST":
        bid_id = request.POST["bidform_search"]
        print bid_id
        bidFormSet = BidForm.objects.filter(bid_id = bid_id)
    else:
        bidFormSet = BidForm.objects.filter(bid_status__part_status = BIDFORM_PART_STATUS_CHECK) 
    
    context = {
        "bidFormSet":bidFormSet,
    }
    return render(request,"purchasing/purchasing_arrival.html",context)

def arrivalCheckViews(request,bid):
    cargo_set = ArrivalInspection.objects.filter(bidform__bid_id = bid)
    context = {
        "cargo_set":cargo_set,
        "bid":bid,
    }
    return render(request,"purchasing/purchasing_arrivalcheck.html",context)

def inventoryTableViews(request):
    order_index = request.GET.get("order_index")
    tableid = request.GET.get("tableid")
    order = WorkOrder.objects.get(order_index = order_index)
    inventoryType = InventoryType.objects.get(id = tableid)
    context = {"order": order,
               "inventoryType": inventoryType,
    }
    return render(request, "purchasing/inventory_table_base.html", context)

def materialEntryViews(request):
    try:
        purchasingentry = PurchasingEntry.objects.get(bidform = 8)
        entry_set = PurchasingEntryItems.objects.filter(purchasingentry = purchasingentry)
        entry_form = EntryForm(instance = purchasingentry)
        print purchasingentry.entry_time
    except Exception,e:
        print e
    context = {
        "pur_entry":purchasingentry,
        "entry_set":entry_set,
        "entry_form":entry_form,
    }
    return render(request,"purchasing/purchasing_materialentry.html",context)

def subApplyHomeViews(request):
    if request.method == "POST":
        receipts_code = request.POST["subapply_search"]
        subapply_set = MaterialSubApply.objects.filter(receipts_code = receipts_code)
    else:
        subapply_set = MaterialSubApply.objects.filter(is_submit = True) 
    context = {
        "subapply_set":subapply_set,
    }
    return render(request,"purchasing/subapply_home.html",context)

@csrf.csrf_protect
def subApplyViews(request,sid = None):
    is_show = False
    subapply_obj = MaterialSubApply.objects.get(id = sid)
    if request.method == "POST":
        subapply_form = SubApplyForm(request.POST,instance = subapply_obj)
        if subapply_form.is_valid():
            subapply_form.save()
            subapply_obj.is_submit = True
            subapply_obj.save()
            return HttpResponseRedirect("/purchasing/subApplyHome/")
    else:
        subapply_form = SubApplyForm(instance = subapply_obj)
    sub_set = MaterialSubApplyItems.objects.filter(sub_apply__id = sid)
    subitem_form = SubApplyItemForm()
    context = {
        "subapply_form":subapply_form,
        "is_show":is_show,
        "sub_set":sub_set,
        "subitem_form":subitem_form,
        "subapply":subapply_obj,
    }
    return render(request,"purchasing/subapplication.html",context)

@csrf.csrf_protect
def subApplyReviewViews(request,sid = None):
    is_show = True
    subapply_obj = MaterialSubApply.objects.get(id = sid)
    if request.method == "POST":
        subapply_form = SubApplyInspectForm(request.POST,instance = subapply_obj)
        if subapply_form.is_valid():
            subapply_form.save()
            subapply_obj.is_submit = True
            subapply_obj.save()
            return HttpResponseRedirect("/purchasing/subApplyHome/")
    else:
        subapply_form = SubApplyInspectForm(instance = subapply_obj)
    sub_set = MaterialSubApplyItems.objects.filter(sub_apply__id = sid)
    subitem_form = SubApplyItemForm()
    context = {
        "subapply_form":subapply_form,
        "is_show":is_show,
        "sub_set":sub_set,
        "subitem_form":subitem_form,
        "subapply":subapply_obj,
    }
    return render(request,"purchasing/subapplication.html",context)
