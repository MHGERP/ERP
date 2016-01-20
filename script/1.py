# coding: UTF-8
from django.shortcuts import render
from django.db.models import Q
from purchasing.models import *
from django.contrib.auth.models import User
from techdata.models import Processing

# a = ContractDetail()
# a.user = User.objects.get(username="123")
# a.amount = 0
# a.bidform = BidForm.objects.get(bid_id="111")
# a.save()

items_all = Processing.objects.all()
for item in items_all:
    print item.operate_date

items = Processing.objects.dates('operate_date', 'month').distinct()

for item in items:
    print "%s-%s"%(item.year,item.month)



