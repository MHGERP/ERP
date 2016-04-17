# coding: UTF-8
from const import *
from django.db import models
from const.models import WorkOrder
from const.utility import make_uuid
import datetime

class SynthesizeFileListStatus(models.Model):
    workorder_id = models.ForeignKey(WorkOrder)
    sketch = models.BooleanField(default = False)
    pressure_test = models.BooleanField(default = False)
    craph = models.BooleanField(default = False)
    product = models.BooleanField(default = False)
    encasement_graph = models.BooleanField(default = False)
    mark = models.BooleanField(default = False)
    encasement_list = models.BooleanField(default = False)
    coating_detail = models.BooleanField(default = False)
    class Meta:
        verbose_name = u"综合工部"
        verbose_name_plural = u"综合工部"
    def __unicode__(self):
        return "%s" % self.workorder_id


class ProductionPlan(models.Model):
    workorder_id = models.ForeignKey(WorkOrder)
    plan_id = models.CharField(max_length=50, blank=True, default=make_uuid, verbose_name=u"生产计划编号")
    status = models.IntegerField(blank = False, choices = PRODUCTION_PLAN_STAUTS_CHOICES, default=2,verbose_name=u"生产计划状态")
    plan_date = models.DateField(blank = True, default=lambda:datetime.datetime.today(), verbose_name = u"计划年月")

    class Meta:
        verbose_name = u"生产计划"
        verbose_name_plural = u"生产计划"
    def __unicode__(self):
        return "%s" % self.plan_id
