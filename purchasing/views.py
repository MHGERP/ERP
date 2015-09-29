from django.shortcuts import render
from purchasing.models import BidForm,ArrivalInspection
from const import *
def purchasingFollowingViews(request):
    """
    chousan1989
    """
    bidform_processing=BidForm.objects.filter(bid_status__status__gte=BIDFORM_STATUS_SELECT_SUPPLIER,bid_status__status__lte=BIDFORM_STATUS_CHECK_STORE)
    context={
        "bidform":bidform_processing,
        "BIDFORM_STATUS_SELECT_SUPPLIER":BIDFORM_STATUS_SELECT_SUPPLIER,
        "BIDFORM_STATUS_INVITE_BID":BIDFORM_STATUS_INVITE_BID,
        "BIDFORM_STATUS_PROCESS_FOLLOW":BIDFORM_STATUS_PROCESS_FOLLOW,
        "BIDFORM_STATUS_CHECK_STORE":BIDFORM_STATUS_CHECK_STORE 
    }

    return render(request,"purchasing/purchasing_following.html",context)


def pendingOrderViews(request):
    context = {}
    return render(request, "purchasing/pending_order.html", context)

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
    suppliers=Supplier.objects.all()
    context={
        "suppliers":suppliers,
    }
    return render(request,"purchasing/supplier/supplier_management.html",context)
def bidTrackingViews(request):
    context = {}
    return render(request, "purchasing/bid_track.html", context)
def arrivalInspectionViews(request):
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
