#coding=UTF-8
from django.db import models
from const.models import WorkOrder
from django.contrib.auth.models import User
from users.models import UserInfo
from const import STORAGEDEPARTMENT_CHOICES,STORAGESTATUS_KEEPER,REFUNDSTATUS_CHOICES
# Create your models here.

class WeldingMaterialApplyCard(models.Model):
    department=models.CharField(verbose_name=u'领用单位',max_length=20,blank=False)
    index=models.IntegerField(verbose_name=u'编号',blank=False,unique=True)
    create_time=models.DateField(verbose_name=u'填写时间',auto_now_add=True)
    workorder=models.ForeignKey(WorkOrder,verbose_name=u'工作令',blank=False)
    weld_bead_number=models.CharField(verbose_name=u'焊缝编号',max_length=20,blank=False)
    weld_material_number=models.CharField(verbose_name=u'焊材标号',max_length=20,blank=False)
    model=models.CharField(verbose_name=u'型号',max_length=20,blank=False)
    standard=models.CharField(verbose_name=u'规格',max_length=20,blank=False)
    apply_weight=models.FloatField(verbose_name=u'领用重量',blank=False)
    apply_quantity=models.FloatField(verbose_name=u'领用数量',blank=False)
    material_number=models.CharField(verbose_name=u'材质编号',max_length=20,blank=False)
    actual_weight=models.FloatField(verbose_name=u'实发重量',default=0,blank=True)
    actual_quantity=models.FloatField(verbose_name=u'实发数量',default=0,blank=True)
    applicant=models.ForeignKey(User,verbose_name=u'领用人',blank=False,related_name="applicants")
    auditor=models.ForeignKey(User,verbose_name=u'审核人',default=None,blank=True,null=True,related_name="auditors")
    inspector=models.ForeignKey(User,verbose_name=u'检查员',default=None,blank=True,null=True,related_name="inspectors")
    commit_user=models.ForeignKey(User,verbose_name=u'发料人',default=None,blank=True,null=True,related_name="commit_users")

    def __unicode__(self):
        return str(self.index)

    class Meta:
        verbose_name=u'焊材领用卡'
        verbose_name_plural=u'焊材领用卡'


class StoreRoom(models.Model):
    name = models.CharField(max_length=20,verbose_name=u"库房名称",blank = False)
    position = models.CharField(max_length=50,verbose_name=u"位置",blank = False)

    def __unicode__(self):
        return "%s"  % self.name

    class Meta:
        verbose_name = u"库房"
        verbose_name_plural = u"库房"

class WeldingMaterialHumitureRecord(models.Model):
    storeRoom = models.ForeignKey(StoreRoom,verbose_name=u"库房")
    storeMan = models.CharField(verbose_name=u'库管员',max_length=20,blank=False)
    demandTemperature = models.CharField(verbose_name=u'要求温度', max_length=20,blank=False)
    demandHumidity = models.CharField(verbose_name=u'要求湿度', max_length=20,blank=False)
    actualTemperature1 = models.FloatField(verbose_name=u'实际温度(10:00)',blank=False)
    actualHumidity1 = models.FloatField(verbose_name=u'实际湿度(10:00)',blank=False)
    actualTemperature2 = models.FloatField(verbose_name=u'实际温度(16:00)',blank=False)
    actualHumidity2 = models.FloatField(verbose_name=u'实际温度(16:00)',blank=False)
    remark = models.CharField(verbose_name=u'备注', max_length=1000,blank=True)
    date = models.DateField(verbose_name = u"日期",auto_now_add=True)
    def __unicode__(self):
        return str(self.date)

    class Meta:
        verbose_name=u'焊材库温湿度记录卡'
        verbose_name_plural=u'焊焊材库温湿度记录卡'

class WeldRefund(models.Model):
    department = models.CharField(max_length=20,choices=STORAGEDEPARTMENT_CHOICES,blank=False,verbose_name=u"退库单位")
    date = models.DateField(blank=False,null=True,verbose_name=u"日期")
    code = models.CharField(max_length=20,blank=False,null=True,unique=True,verbose_name=u"编号")
    work_order = models.ForeignKey(WorkOrder,verbose_name=u"工作令")
    receipts_time = models.DateField(blank=False,null=True,verbose_name=u"领用日期")
    receipts_code = models.CharField(max_length=20,blank=False,null=True,verbose_name=u"领用编号")
    refund_weight = models.FloatField(default=0,blank=False,verbose_name=u"退库量（重量）")
    refund_count = models.FloatField(default=0,blank=False,verbose_name=u"退库量（数量）")
    refund_status = models.CharField(max_length=20,blank=False,null=True,verbose_name=u"退库状态")
    weldrefund_status = models.IntegerField(default=STORAGESTATUS_KEEPER,choices=REFUNDSTATUS_CHOICES,verbose_name=u"退库单状态")
    refunder =  models.ForeignKey(User,verbose_name=u"退库人",related_name = "weldrefund_refunder")
    keeper = models.ForeignKey(User,verbose_name=u"库管人",related_name = "weldrefund_keeper")   
    
    class Meta:
        verbose_name = u"焊接材料退库卡"
        verbose_name_plural = u"焊接材料退库卡"

    def __unicode__(self):
        return '%s' % self.code
