# coding: UTF-8
from django.shortcuts import render
from django.db import connection
from django.db.models import Q, Sum
from const import *
from purchasing.models import *
from techdata.models import *
from production.models import *
from django.contrib.auth.models import User
from const.models import *
import datetime

PRODUCTIONGROUP_PROCESS = (
        ("F",  102),
        ("X",  101),
        ("P",  104),
        ("D",  110),
        ("D",  188),
        ("G2", 103),
        ("G3", 113),
        ("G",  111),
        ("M",  "m"),
        ("B",  105),
        ("K",  109),
        ("W",  108),
        ("W",  106),
        ("J", "j"),
        ("Z",  "z"),
        ("H",  "h"),
        ("L",  "l"),
)


def importProductionWorkGroup():
    processdict = {}
    for (k, v) in PROCESSING_CHOICES:
        processdict[v] = k
    for (k, v) in PRODUCTIONGROUP_PROCESS:
        try:
            processname = ProcessingName.objects.get(name = processdict[k])
            workgroup = ProductionWorkGroup(name = v, processname = processname)
            print k,v
            workgroup.save()
        except:
            pass

def importProcessDetail():
    process = Processing.objects.get(materiel_belong__id = 31)
    subMateriel = SubMateriel.objects.get(id=1)
    print process
    for i in xrange(1,13):
        #setattr(process, "GS%d" %i, i*10)
        item = ProcessDetail(sub_materiel_belong = subMateriel, processname = getattr(process, "GX%d" %i), work_hour = int(getattr(process, "GS%d" %i)), process_id = i, complete_process_date=datetime.datetime.today())
        item.save()
    print "help"

importProcessDetail()
print "hello"
