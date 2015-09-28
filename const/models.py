# coding: UTF-8
from django.db import models
from const import *

class WorkOrder(models.Model):
    order_index = models.CharField(blank = False, unique = True, max_length = 20, verbose_name = u"工作令编号")
    sell_type = models.IntegerField(blank = False, choices = SELL_TYPE, verbose_name = "销售类型")
    client_name = models.CharField(blank = False, max_length = 20, verbose_name = "客户名称")
    product_name = models.CharField(blank = False, max_length = 20, verbose_name = "产品名称")
    class Meta:
        verbose_name = u"工作令"
        verbose_name_plural = u"工作令"
    def __unicode__(self):
        return self.order_index

class BidFormStatus(models.Model):
    #status=models.IntegerField(blank=False,unique=True,choices=BIDFORM_STATUS_CHOICES,verbose_name=u"标单状态")
    main_status=models.IntegerField(blank=False,choices=BIDFORM_STATUS_CHOICES,verbose_name=u"标单状态")
    part_status=models.IntegerField(blank=False,unique=True,choices=BIDFORM_PART_STATUS_CHOICES,verbose_name=u"子状态")
    next_part_status=models.ForeignKey('self',null=True,blank=True)
    class Meta:
        verbose_name = u"标单状态"
        verbose_name_plural = u"标单状态"
    def __unicode__(self):
        return self.get_part_status_display()
