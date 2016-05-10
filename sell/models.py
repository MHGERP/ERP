#coding: utf=8
from django.db import models
from users.models import Group
import settings

class BidFile(models.Model):
    recv_group = models.ForeignKey(Group, verbose_name = u"下发部门")
    file_obj = models.FileField(upload_to = settings.SELL_BIDFILE_PATH + "/%Y/%m/%d", verbose_name = u"招标文件")
    name = models.CharField(max_length = 100, blank = False, verbose_name = u"文件名称")
    upload_date = models.DateTimeField(null = True, blank = True, verbose_name = u"上传时间")
    file_size = models.CharField(max_length = 50, blank = True, null = True, default = None, verbose_name = u"文件大小")
    class Meta:
        verbose_name = u"招标文件"
        verbose_name_plural = u"招标文件"
    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 50, verbose_name = u"产品名称")
    #down : sell group to others, up : others to sell
    manufacture_file_down = models.OneToOneField(BidFile, null = True, blank = True, verbose_name = u"生产科文件", related_name = "manufacture_file")
    techdata_file_down = models.OneToOneField(BidFile, null = True, blank = True, verbose_name = u"工艺科文件", related_name = "techdata_file")
    purchasing_file_down = models.OneToOneField(BidFile, null = True, blank = True, verbose_name = u"采购科文件", related_name = "purchasing_file")
    manufacture_file_up = models.OneToOneField(BidFile, null = True, blank = True, verbose_name = u"生产科文件", related_name = "manufacture_file")
    techdata_file_up = models.OneToOneField(BidFile, null = True, blank = True, verbose_name = u"工艺科文件", related_name = "techdata_file")
    purchasing_file_up = models.OneToOneField(BidFile, null = True, blank = True, verbose_name = u"采购科文件", related_name = "purchasing_file")
    class Meta:
        verbose_name = u"产品"
        verbose_name_plural = u"产品"
    def __unicode__(self):
        return self.name


