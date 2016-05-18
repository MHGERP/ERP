# coding: UTF-8
from django.shortcuts import render
from django.db import connection
from django.db.models import Q, Sum
from purchasing.models import *
from django.contrib.auth.models import User
from production.models import *
from const.models import Materiel
from production.utility import get_applycard_code
from storage.models import SteelMaterialApplyCard, OutsideApplyCard

print get_applycard_code(OutsideApplyCard)
print "hello"
# items_list = ProcessDetail.objects.filter(complete_process_date__isnull = 1).order_by('-productionworkgroup');
# print items_list.count()
# items_list = ProcessDetail.objects.filter(complete_process_date__isnull = 0).order_by('-productionworkgroup');
# print items_list.count()
# synthesize = SynthesizeFileListStatus.objects.filter(order_id = 1).values("sketch","encasement_list", "coating_detail")
# print synthesize
# for k,v in synthesize[0].items():
#     print k,v


# select = {'month': connection.ops.date_trunc_sql('month', 'complete_process_date')}
# process_detail_list  = ProcessDetail.objects.extra(select=select).values( 'month', 'materiel_belong__order__order_index', 'materiel_belong__order', 'productionworkgroup__name', 'productionworkgroup#' )
# print process_detail_list
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

# print "hello"

# materiels = Materiel.objects.filter(Q(index__in = [55,56]))

# for item in materiels:
#     print item.index
