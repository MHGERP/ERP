# coding: UTF-8
from django.shortcuts import render
from django.db import connection
from django.db.models import Q, Sum
from purchasing.models import *
from django.contrib.auth.models import User
from techdata.models import Processing

# a = ContractDetail()
# a.user = User.objects.get(username="123")
# a.amount = 0
# a.bidform = BidForm.objects.get(bid_id="111")
# a.save()

#items = Processing.objects.dates('operate_date', 'month').distinct()

select = {'month': connection.ops.date_trunc_sql('month', 'operate_date')}
items = Processing.objects.extra(select=select).values('materiel_belong__order', 'operator', 'month').annotate(Sum('hour'))

print items.count()
for item in items:
    print item

print "hello"
