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
