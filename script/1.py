# coding: UTF-8
from django.shortcuts import render
from django.db import connection
from django.db.models import Q, Sum
from purchasing.models import *
from django.contrib.auth.models import User
from techdata.models import Processing
from const.models import Materiel

# a = ContractDetail()
# a.user = User.objects.get(username="123")
# a.amount = 0
# a.bidform = BidForm.objects.get(bid_id="111")
# a.save()

# items_all = Processing.objects.all()
# for item in items_all:
#     print item.operate_date

# items = Processing.objects.dates('operate_date', 'month').distinct()

# for item in items:
#     print "%s-%s"%(item.year,item.month)

#items = Processing.objects.dates('operate_date', 'month').distinct()

# select = {'month': connection.ops.date_trunc_sql('month', 'operate_date')}
# items = Processing.objects.extra(select=select).values('materiel_belong__order', 'operator', 'month').annotate(Sum('hour'))
# values('materiel_belong', 'operator', 'month').annotate(Sum('hour'))
# Processing.objects.filter(Q)
# print items.count()
# for item in items:
#     print item

print "hello"

materiels = Materiel.objects.filter(Q(index__in = [55,56]))

for item in materiels:
    print item.index

print "hello"
