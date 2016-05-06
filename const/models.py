# coding: UTF-8
from django.db import models
from const import *
from django.contrib.auth.models import User

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
    name = models.CharField(blank = False, max_length = 50, verbose_name = u"材质名称")
    material_id= models.CharField(blank = True, null = True , max_length = 20, verbose_name = u"材质编号") 
    categories =  models.CharField(blank = True, null = True , choices = MATERIAL_CATEGORY_CHOICES, max_length = 20, verbose_name = u"材料类别")
    class Meta:
        verbose_name = u"材料"
        verbose_name_plural = u"材料"
    def __unicode__(self):
        return self.name

class InventoryType(models.Model):
    name = models.CharField(blank = False, max_length = 50, choices = INVENTORY_TYPE, verbose_name = u"明细表名称")
    class Meta:
        verbose_name = u"明细表类别"
        verbose_name_plural = u"明细表类别"
    def __unicode__(self):
        return self.get_name_display()

class Materiel(models.Model):
    order = models.ForeignKey(WorkOrder, blank = True, null = True, verbose_name = u"所属工作号")
    index = models.CharField(blank = True, max_length = 20, verbose_name = u"票号")
    sub_index = models.CharField(blank = True, null = True, max_length = 20, verbose_name = u"部件号")
    schematic_index = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"图号")
    parent_schematic_index = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"部件图号")
    parent_name = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"部件名称")
    material = models.ForeignKey(Material, blank = True, null = True, verbose_name = u"材料")
    name = models.CharField(blank = False, max_length = 100, verbose_name = u"名称")
    count = models.CharField(blank = True, max_length = 20, null = True, verbose_name = u"数量")
    net_weight = models.FloatField(blank = True, null = True, verbose_name = u"净重")
    total_weight = models.FloatField(blank = True, null = True, verbose_name = u"毛重")
    quota = models.FloatField(blank = True, null = True, verbose_name = u"定额")
    quota_coefficient = models.FloatField(blank = True, null = True, verbose_name = u"定额系数")
    inventory_type = models.ManyToManyField(InventoryType, blank = True, null = True, verbose_name = u"明细表归属")
    remark = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"备注")
    specification = models.CharField(blank = True, null = True , max_length = 20, verbose_name = u"规格")
    standard = models.CharField(blank = True, null = True , max_length = 20, verbose_name = u"标准") 
    unit = models.CharField(blank = True, null = True , max_length = 20, verbose_name = u"单位") 
    status = models.CharField(blank = True, null = True , max_length = 20, verbose_name = u"状态")
    press=models.CharField(blank=True,null=True,max_length=20,verbose_name=u"受压")
    recheck=models.CharField(blank=True,null=True,max_length=20,verbose_name=u"复验")
    detection_level=models.CharField(blank=True,null=True,max_length=20,verbose_name=u"探伤级别")
    
    complete_plandate = models.DateField(blank = True, null=True,verbose_name = u"计划完成时间")
    complete_date = models.DateField(blank = True, null=True,verbose_name = u"完成时间")
    
    class Meta:
        verbose_name = u"物料"
        verbose_name_plural = u"物料"
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

class OrderFormStatus(models.Model):
    status = models.IntegerField(blank = False, choices = ORDERFORM_STATUS_CHOICES, verbose_name = u"订购单状态")
    next_status = models.ForeignKey('self', null = True, blank = True)
    class Meta:
        verbose_name = u"订购单状态"
        verbose_name_plural = u"订购单状态"
    def __unicode__(self):
        return self.get_status_display()

class ImplementClassChoices(models.Model):
    category = models.IntegerField(blank = False, choices = IMPLEMENT_CLASS_CHOICES, verbose_name = u"实施类别")
    class Meta:
        verbose_name = u"实施类别"
        verbose_name_plural = u"实施类别"
    def __unicode__(self):
        return self.get_category_display()


