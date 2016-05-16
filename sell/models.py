#coding: utf=8
from const import REVIEW_COMMENTS_CHOICES
from django.db import models
from users.models import Group
import settings

class BidFile(models.Model):
    recv_group = models.ForeignKey(Group, null = True, blank = True, verbose_name = u"下发部门")
    file_obj = models.FileField(upload_to = settings.SELL_BIDFILE_PATH + "/%Y/%m/%d", verbose_name = u"招标文件")
    name = models.CharField(max_length = 100, blank = False, verbose_name = u"文件名称")
    upload_date = models.DateTimeField(null = True, blank = True, verbose_name = u"上传时间")
    file_size = models.CharField(max_length = 50, blank = True, null = True, default = None, verbose_name = u"文件大小")
    is_approval = models.IntegerField(choices = REVIEW_COMMENTS_CHOICES, default = -1, verbose_name = u"招标文件审核结果", blank = False)
    #False: sell to others, down                False: others to sell up
    file_type = models.BooleanField(default = False, verbose_name = u"文件类型")
    class Meta:
        verbose_name = u"招标文件"
        verbose_name_plural = u"招标文件"
    def __unicode__(self):
        return self.name
    def getStatus(self):
        return self.get_is_approval_display()

class Product(models.Model):
    name = models.CharField(max_length = 50, verbose_name = u"产品名称")
    #down : sell group to others, up : others to sell
    manufacture_file_down = models.OneToOneField(BidFile, null = True, blank = True, verbose_name = u"生产科下发文件", related_name = "manufacture_file_down")
    techdata_file_down = models.OneToOneField(BidFile, null = True, blank = True, verbose_name = u"工艺科下发文件", related_name = "techdata_file_down")
    purchasing_file_down = models.OneToOneField(BidFile, null = True, blank = True, verbose_name = u"采购科下发文件", related_name = "purchasing_file_down")
    manufacture_file_up = models.OneToOneField(BidFile, null = True, blank = True, verbose_name = u"生产科回传文件", related_name = "manufacture_file_up")
    techdata_file_up = models.OneToOneField(BidFile, null = True, blank = True, verbose_name = u"工艺科回传文件", related_name = "techdata_file_up")
    purchasing_file_up = models.OneToOneField(BidFile, null = True, blank = True, verbose_name = u"采购科回传文件", related_name = "purchasing_file_up")
    is_approval = models.IntegerField(choices = REVIEW_COMMENTS_CHOICES, default = -1, verbose_name = u"产品审核结果", blank = False)
    is_finish = models.BooleanField(default = False, verbose_name = u"是否终止")
    class Meta:
        verbose_name = u"产品"
        verbose_name_plural = u"产品"
    def __unicode__(self):
        return self.name
    def getStatus(self):
        return self.get_is_approval_display()

