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


class Supplier(models.Model):
    supplier_id=models.CharField(unique=True,max_length=20,blank=False,verbose_name=u"供应商编号")
    supplier_name=models.CharField(max_length=50,blank=False,verbose_name=u"供应商名称")
    class Meta:
        verbose_name = u"供应商"
        verbose_name_plural = u"供应商"
    def __unicode__(self):
        return '%s'% (self.supplier_name)

import settings
class SupplierFile(models.Model):

    project = models.ForeignKey(Supplier)
    name = models.CharField(max_length=100, blank=False, verbose_name="文件名称")
    file_obj = models.FileField(upload_to=settings.PROCESS_FILE_PATH +"/%Y/%m/%d",verbose_name="文件对象")
    upload_time = models.DateTimeField(blank=True, null=True,verbose_name="上传时间")
    file_size = models.CharField(max_length=50, blank=True, null=True,default=None, verbose_name="文件大小")
    file_type = models.CharField(max_length=50, blank=True, null=True,default=None, verbose_name="文件类型")

    class Meta:
        verbose_name = "文件上传"
        verbose_name_plural = "文件上传"

    def __unicode__(self):
        return self.name 

