# coding: UTF-8
from django.db import models
from const.models import BidFormStatus

# Create your models here.
class BidForm(models.Model):
    bid_id=models.CharField(unique=True,max_length=20,blank=False,verbose_name=u"标单编号")
    create_time=models.DateTimeField(null=True,verbose_name=u"创建日期")
    establishment_time=models.DateTimeField(null=True,verbose_name=u"编制日期")
    audit_time=models.DateTimeField(null=True,verbose_name=u"审核日期")
    approved_time=models.DateTimeField(null=True,verbose_name=u"批准日期")
    bid_status=models.ForeignKey(BidFormStatus,null=False,verbose_name=u"标单状态")
    class Meta:
        verbose_name = u"标单"
        verbose_name_plural = u"标单"
    def __unicode__(self):
        return '%s'% (self.bid_id)

class bidApply(models.Model):
    apply_id = models.CharField(unique=True, max_length=20, blank=False, verbose_name=u"标单申请编号")
    apply_company = models.CharField(null=True, verbose_name=u"申请单位")
    demand_company = models.CharField(null=True, verbose_name=u"需求单位")
    work_order = models.ForeignKey(BidFormStatus,null=False,verbose_name=u"工作令")
    amount = models.IntegerField(defaults=0, verbose_name=u"数量")
    bid_project = models.CharField(null=True, verbose_name=u"拟招(议)项目")
    bid_date = models.DateTimeField(null=True,verbose_name=u"拟招(议)标时间")
    special_model = models.CharField(null=True, verbose_name=u"规格、型号")
    core_part = models.BooleanField(defaults=False, verbose_name="是否为核心件")

    class Meta:
        verbose_name = u"标单申请表"

    def __unicode__(self):
        return '%s'% (self.apply_id)

class qualityPriceCard(models.Model):
    apply_id = models.CharField(unique=True, max_length=20, blank=False, verbose_name=u"标单申请编号")
    apply_company = models.CharField(null=True, verbose_name=u"申请单位")
    demand_company = models.CharField(null=True, verbose_name=u"需求单位")
    work_order = models.ForeignKey(BidFormStatus,null=False,verbose_name=u"工作令")
    amount = models.IntegerField(defaults=0, verbose_name=u"数量")
    unit = models.CharField(null=True, verbose_name=u"单位")
    content = models.CharField(null=True, verbose_name=u"内容")
    material = models.CharField(null=True, verbose_name=u"材质")
    delivery_period = models.CharField(null=True, verbose_name=u"交货期")
    price = models.CharField(null=True, verbose_name=u"价格")
    ability = models.CharField(null=True, verbose_name=u"厂家协作能力质量情况及业绩")
    delivery_condition = models.CharField(null=True, verbose_name=u"交货及支付条件")
    class Meta:
        verbose_name = u"标单申请表"

    def __unicode__(self):
        return '%s'% (self.apply_id)

class ArrivalInspection(models.Model):
    material_confirm = models.BooleanField(null=False,default=False,verbose_name=u"实物确认")
    soft_confirm = models.BooleanField(null=False,default=False,verbose_name=u"软件确认")
    inspect_confirm = models.BooleanField(null=False,default=False,verbose_name=u"检验通过")
    bidform = models.ForeignKey(BidForm,null=False,verbose_name=u"标单号")
    class Meta:
        verbose_name = u"到货检验"
        verbose_name_plural = u"到货检验"

    def __unicode__(self):
        return '%s' % self.bidform.bid_id
