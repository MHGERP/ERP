# coding: UTF-8
from const import *
from django.db import models
from const.models import *
from django.contrib.auth.models import User
from const.utility import make_uuid
from techdata.models import ProcessingName
from users.models import UserInfo
import datetime

class ProductionWorkGroup(models.Model):
    name = models.CharField(blank = False, null = False , max_length = 20, verbose_name = u"名字")
    processname = models.ForeignKey(ProcessingName, blank = False, null = False, verbose_name = u"工序")
    class Meta:
        verbose_name = u"生产工作组"
        verbose_name_plural = u"生产工作组"
    def __unicode__(self):
        return self.name

class ProductionUser(models.Model):
    production_user_id = models.OneToOneField(UserInfo,verbose_name=u"生产人员")
    production_work_group = models.ForeignKey(ProductionWorkGroup,blank=True, null=True, verbose_name=u"所属工作组")
    class Meta:
        verbose_name = "生产人员账户"
        verbose_name_plural = "生产人员账户"
    def __unicode__(self):
        return '%s' % (self.production_user_id.name)

class ProcessDetail(models.Model):
    materiel_belong = models.ForeignKey(Materiel, blank = False, verbose_name = u"工作票")
    processname = models.ForeignKey(ProcessingName, blank = False, verbose_name = u"工序名称")
    process_id = models.IntegerField(blank=False, verbose_name=u"第几道工序")
    work_hour = models.IntegerField(blank=False, verbose_name=u"工时")
    productionworkgroup = models.ForeignKey(ProductionWorkGroup, blank = True, null = True, verbose_name = u"工作组")
    plan_startdate = models.DateField(blank = True, null= True, verbose_name = u"计划开始时间")
    plan_enddate = models.DateField(blank = True, null= True, verbose_name = u"计划完成时间")
    complete_date = models.DateField(blank = True, null= True, verbose_name = u"完成时间")
    check_user = models.ForeignKey(User, null = True, verbose_name = u"检查者")
    check_date = models.DateField(blank = True, null= True, verbose_name = u"检查时间")
    check_content = models.CharField(blank = True,  null= True, max_length = 500, verbose_name = u"检查内容")

    class Meta:
        verbose_name = u"工序详细信息"
        verbose_name_plural = u"工序详细信息"
        unique_together = ("materiel_belong", "process_id")
    def __unicode__(self):
        return u"%s-%d-%s" % (self.materiel_belong, self.process_id, self.processname)

class SynthesizeFileListStatus(models.Model):
    order = models.ForeignKey(WorkOrder, verbose_name = u"工作令")
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
    order = models.ForeignKey(WorkOrder, verbose_name = u"工作令")
    plan_id = models.CharField(max_length=50, blank=True, default=make_uuid, verbose_name=u"生产计划编号")
    status = models.IntegerField(blank = False, choices = PRODUCTION_PLAN_STAUTS_CHOICES, default=2,verbose_name=u"生产计划状态")
    plan_date = models.DateField(blank = True, default=lambda:datetime.datetime.today(), verbose_name = u"计划年月")

    class Meta:
        verbose_name = u"生产计划"
        verbose_name_plural = u"生产计划"
    def __unicode__(self):
        return "%s" % self.plan_id
