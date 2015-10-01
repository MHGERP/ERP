# coding: UTF-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from purchasing.models import BidForm,ArrivalInspection,Supplier
from const import *
from django.template.loader import render_to_string
from django.utils import simplejson
from const.models import WorkOrder
from const.forms import InventoryTypeForm

@dajaxice_register
def searchPurchasingFollowing(request,bidid):
    bidform_processing=BidForm.objects.filter(bid_id=bidid)
    context={
        "bidform":bidform_processing,
        "BIDFORM_STATUS_SELECT_SUPPLIER":BIDFORM_STATUS_SELECT_SUPPLIER,
        "BIDFORM_STATUS_INVITE_BID":BIDFORM_STATUS_INVITE_BID,
        "BIDFORM_STATUS_PROCESS_FOLLOW":BIDFORM_STATUS_PROCESS_FOLLOW,
        "BIDFORM_STATUS_CHECK_STORE":BIDFORM_STATUS_CHECK_STORE 
    }
    purchasing_html=render_to_string("purchasing/purchasingfollowing/purchasing_following_table.html",context)
    data={
        'html':purchasing_html
    }
    return simplejson.dumps(data)

@dajaxice_register
def checkArrival(request,aid,cid):
    arrivalfield = ARRIVAL_CHECK_FIELDS[cid]
    cargo_obj = ArrivalInspection.objects.get(id = aid)
    val = not getattr(cargo_obj,arrivalfield)
    setattr(cargo_obj,arrivalfield,val)
    cargo_obj.save()
    val = getattr(cargo_obj,arrivalfield)
    data = {
        "flag":val, 
    }
    return simplejson.dumps(data)

@dajaxice_register
def genEntry(request,bid):
    flag = isAllChecked(bid)
    data = {
        'flag':flag,
    }
    print flag
    return simplejson.dumps(data)

@dajaxice_register
def SupplierUpdate(request,supplier_id):
    supplier=Supplier.objects.get(supplier_id=supplier_id)

    supplier_html=render_to_string("purchasing/supplier/supplier_file_table.html",{"supplier":supplier})
    return simplejson.dumps({'supplier_html':supplier_html})
def isAllChecked(bid):
    cargo_set = ArrivalInspection.objects.filter(bidform__bid_id = bid)
    for cargo_obj in cargo_set:
        for key,field in ARRIVAL_CHECK_FIELDS.items():
            val = getattr(cargo_obj,field)
            if not val:
                return False
    return True

@dajaxice_register
def pendingOrderSearch(request, order_index):
    """
    JunHU
    summary: ajax function to search the order set by order index
    params: order_index: the index of the work order
    return: table html string
    """
    inventoryTypeForm = InventoryTypeForm()
    orders = WorkOrder.objects.filter(order_index__startswith = order_index)
    context = {"inventoryTypeForm": inventoryTypeForm,
               "orders": orders
              }
    html = render_to_string("purchasing/pending_order/pending_order_table.html", context)
    return html

@dajaxice_register
def getInventoryTable(request, table_id, order_index):
    context = {}
    html = render_to_string("purchasing/inventory_table/main_materiel.html", context)
    return html
