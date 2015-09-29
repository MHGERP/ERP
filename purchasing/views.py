from django.shortcuts import render
from purchasing.models import BidForm,ArrivalInspection
from const import *
from const.forms import InventoryTypeForm
from const.models import WorkOrder
from purchasing.forms import SupplierForm

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

def selectSupplierViews(request):
    context={}
    return render(request,"purchasing/select_supplier.html",context)

def supplierManagementViews(request):
    suppliers=Supplier.objects.all()
    supplier_form=SupplierForm()
    context={
        "suppliers":suppliers,
        "supplier_form":supplier_form
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
