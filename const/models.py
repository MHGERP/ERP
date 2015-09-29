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

class Material(models.Model):
    name = models.CharField(blank = False, max_length = 50, verbose_name = u"材料名称")
    class Meta:
        verbose_name = u"材料"
        verbose_name_plural = u"材料"
    def __unicode__(self):
        return self.name

class InventoryType(models.Model):
    name = models.CharField(blank = False, max_length = 50, verbose_name = u"明细表名称")
    class Meta:
        verbose_name = u"明细表类别"
        verbose_name_plural = u"明细表类别"
    def __unicode__(self):
        return self.name

class Materiel(models.Model):
    order = models.ForeignKey(WorkOrder, blank = False, verbose_name = u"所属工作号")
    index = models.CharField(blank = True, max_length = 20, verbose_name = u"编号")
    schematic_index = models.CharField(blank = False, max_length = 50, verbose_name = u"零件图号")
    parent_schematic_index = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"部件图号")
    material = models.ForeignKey(Material, verbose_name = u"材料")
    name = models.CharField(blank = False, max_length = 20, verbose_name = u"名称")
    count = models.CharField(blank = True, max_length = 20, null = True, verbose_name = u"数量")
    net_weight = models.FloatField(blank = True, null = True, verbose_name = u"净重")
    total_weight = models.FloatField(blank = True, null = True, verbose_name = u"总重")

    inventory_type = models.ForeignKey(InventoryType, blank = True, null = True, verbose_name = u"明细表归属")
    class Meta:
        verbose_name = u"物料"
        verbose_name_plural = u"物料"
    def __unicode__(self):
        return self.name

class CirculationName(models.Model):
    name = models.CharField(blank = False, max_length = 10, verbose_name = u"流转简称")
    full_name = models.CharField(blank = False, max_length = 10, verbose_name = u"流转名称全称")
    class Meta:
        verbose_name = u"流转名称"
        verbose_name_plural = u"流转名称"
    def __unicode__(self):
        return self.full_name

class CirculationRoute(models.Model):
    materiel_belong = models.ForeignKey(Material, blank = False, verbose_name = u"所属物料")
    index = models.IntegerField(blank = False, choices = INDEX_LIST, verbose_name = u"流转序号")
    name = models.ForeignKey(CirculationName, blank = False, verbose_name = u"流转名称")
    class Meta:
        verbose_name = u"流转路线"
        verbose_name_plural = u"流转路线"
    def __unicode__(self):
        return self.name

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
