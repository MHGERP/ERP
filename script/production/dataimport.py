# coding: UTF-8
from django.shortcuts import render
from django.db import connection
from django.db.models import Q, Sum
from purchasing.models import *
from production.models import *
from django.contrib.auth.models import User
from techdata.models import Processing
from const.models import *

def importProcessDetail():
    process = Processing.objects.get(materiel_belong__id = 226)
    print process
    for i in xrange(1,13):
        item = ProcessDetail(materiel_belong = process.materiel_belong, processname = getattr(process, "GX%d" %i), work_hour = int(getattr(process, "GS%d" %i)), process_id = i)
        item.save()
    print "help"

importProcessDetail()
print "hello"
