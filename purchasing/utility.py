# coding: UTF-8
from datetime import datetime
from purchasing.models import StatusChange
from const.models import BidFormStatus
from const import *

def goNextStatus(bidform,user):
    original_status=bidform.bid_status
    new_status=original_status.next_part_status
    change_time=datetime.now()
    status_change=StatusChange(bidform=bidform,original_status=original_status,new_status=new_status,change_user=user,change_time=change_time)
    status_change.save()
    bidform.bid_status=new_status
    bidform.save()

def goStopStatus(bidform,user):
    original_status=bidform.bid_status
    new_status=BidFormStatus.objects.get(part_status=BIDFORM_STATUS_STOP)
    change_time=datetime.now()
    status_change=StatusChange(bidform=bidform,original_status=original_status,new_status=new_status,change_user=user,change_time=change_time,normal_change=False)
    status_change.save()
    bidform.bid_status=new_status
    bidform.save()
