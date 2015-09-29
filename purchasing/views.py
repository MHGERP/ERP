from django.shortcuts import render
from purchasing.models import BidForm
from const import *
from const.forms import InventoryTypeForm
from const.models import WorkOrder

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
    """
    JunHU
    summary: view function of pendingorder page
    params: NULL
    return: NULL
    """
    inventoryTypeForm = InventoryTypeForm
    orders = WorkOrder.objects.all()
    context = {"inventoryTypeForm": inventoryTypeForm,
               "orders": orders,}
    return render(request, "purchasing/pending_order.html", context)

def arrivalInspectionViews(request):
    bidFormSet = BidForm.objects.filter(bid_status__part_status = BIDFORM_PART_STATUS_CHECK) 
    
    context = {
        "bidFormSet":bidFormSet,
    }
    return render(request,"purchasing/purchasing_arrival.html",context)
