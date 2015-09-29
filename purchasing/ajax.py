# coding: UTF-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from purchasing.models import BidForm,ArrivalInspection 
from const import *
from django.template.loader import render_to_string
from django.utils import simplejson

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
def checkArrival(request,bid):
    cargo_set = ArrivalInspection.objects.filter(bidform__bid_id = bid)
    print cargo_set
    context = {
        "cargo_set":cargo_set,
    }
    arrival_table_html = render_to_string("purchasing/widgets/arrivalinspection_table.html",context)
    data = {
        "arrival_table_html":arrival_table_html,
    }
    return simplejson.dumps(data)
