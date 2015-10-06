# coding: UTF-8
from django.shortcuts import render
from purchasing.models import BidForm,ArrivalInspection,Supplier,PurchasingEntry,\
    PurchasingEntryItems,SupplierFile,MaterialSubApply,MaterialSubApplyItems
from const import *
from const.forms import InventoryTypeForm
from const.models import WorkOrder, InventoryType
from purchasing.forms import SupplierForm, BidApplyForm, QualityPriceCardForm

from purchasing.forms import SupplierForm,EntryForm
from datetime import datetime
from django.template import RequestContext
from django.views.decorators import csrf
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
    """
    Liu Ye
    """
    qualityPriceCardForm = QualityPriceCardForm()
    bidApplyForm = BidApplyForm()

    bid_status = []
    bid_status.append({"name":u"招标申请表",         "class":"btn-success"})
    bid_status.append({"name":u"分公司领导批准",     "class":"btn-success"})
    bid_status.append({"name":u"滨海公司领导批准",   "class":""})
    bid_status.append({"name":u"滨海招标办领导批准", "class":"btn-danger"})
    bid_status.append({"name":u"中标通知书",         "class":""})
    context = {"bid_status": bid_status,
               "qualityPriceCardForm": qualityPriceCardForm,
               "bidApplyForm": bidApplyForm,
             }
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

def subApplyViews(request):
    if request.method == "POST":
        sub_id = request.POST["subapply_search"]
        subapply_set = MaterialSubApply.objects.filter(id = sub_id)
    subapply_set = MaterialSubApply.objects.all() 
    context = {
        "subapply_set":subapply_set,
    }
    return render(request,"purchasing/subapply_home.html",context)
