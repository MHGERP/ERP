#coding=UTF-8
from django.db import models
from const.models import WorkOrder
from django.contrib.auth.models import User
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


class SteelMaterialPurchasingEntry(models.Model):
    material_source = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'货物来源')
    form_code = models.CharField(max_length=20,blank=False,null=False,verbose_name="入库单编号")
    purchaser =  models.ForeignKey(User,blank=False,null=False,related_name = "purchaser",verbose_name=u"采购员")
    inspector = models.ForeignKey(User,blank=False,null=False,related_name = "inspector",verbose_name=u"检验员",)
    keeper = models.ForeignKey(User,blank=False,null=False,related_name = "keeper",verbose_name=u"库管员" ,)
    remark = models.CharField(max_length=50,blank=True,null=True,verbose_name="备注")
    entry_time = models.DateField(blank=False,null=True,auto_now_add=True,verbose_name=u"入库时间")
    entry_confirm = models.BooleanField(default=False,verbose_name=u"入库单确认")
    entry_type = models.IntegerField(choices = ENTRYTYPE_CHOICES_2,default=0,verbose_name=u"入库单类型")
    entry_status = models.IntegerField(choices=ENTRYSTATUS_CHOICES,default=0,verbose_name=u"入库单状态")

    def __unicode__(self):
        return str(self.form_code)

    class Meta:
        verbose_name=u'钢材入库单'
        verbose_name_plural=u'钢材入库单'

class SteelMaterial(models.Model):
    name = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'材料名称')
    specifications = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'规格')
    batch_number = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'炉号')
    lot_number = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'批号')
    material_number = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'材质编号')
    return_time = models.IntegerField(default=0,verbose_name=u'退库次数')
    entry_form = models.ForeignKey(SteelMaterialPurchasingEntry,blank=False,null=False,verbose_name=u'表头')
    work_order = models.ManyToManyField(WorkOrder,blank=False,null=False,verbose_name=u'工作令')

    def __unicode__(self):
        return str(self.name)+'('+str(self.specifications)+')'

    class Meta:
        verbose_name=u'钢材参数信息'
        verbose_name_plural=u'钢材参数信息'

class BoardSteelMaterialLedger(models.Model):
    material_info = models.ForeignKey(SteelMaterial,blank=False,null=False,verbose_name="钢材信息")
    quantity = models.IntegerField(blank=False,null=False,verbose_name=u'钢板数量')
    weight = models.FloatField(blank=False,null=False,verbose_name=u'钢板重量',default=0)
    weight_management = models.IntegerField(choices=WEIGHT_MANAGEMENT,default=0,blank=False,null=False,verbose_name=u'重量单位')
    area = models.FloatField(blank=False,null=False,verbose_name=u'钢板面积',default=0)
    area_management = models.IntegerField(choices=AREA_MANAGEMENT,default=0,blank=False,null=False,verbose_name=u'面积单位')
    store_room = models.ForeignKey(StoreRoom,blank=False,null=False,verbose_name=u'库房位置')
    slice_cad = models.CharField(max_length=50,blank=True,null=True,verbose_name=u'套料图')

    def __unicode__(self):
        return str(self.material_info)

    class Meta:
        verbose_name=u'板材台账'
        verbose_name_plural=u'板材台账'

class BarSteelMaterialLedger(models.Model):
    material_info = models.ForeignKey(SteelMaterial,blank=False,null=False,verbose_name=u"钢材信息")
    quantity = models.IntegerField(blank=False,null=False,verbose_name=u'型材数量')
    store_room = models.ForeignKey(StoreRoom,blank=False,null=False,verbose_name=u'库房位置')
    length = models.FloatField(blank=True,null=True,verbose_name=u"长度",default=0)
    length_management = model.IntegerField(choices=LENGTH_MANAGEMENT,default=0,verbose_name=u"长度单位")

    def __unicode__(self):
        return str(self.material_info)

    class Meta:
        verbose_name=u'型材台账'
        verbose_name_plural=u'型材台账'

class CommonSteelMaterialReturnCardInfo(models.Model):
    work_order=models.ForeignKey(WorkOrder,blank=False,null=False,verbose_name=u"工作令")
    date = models.DateField(blank=False,null=False,auto_now_add=True,verbose_name=u"日期")
    form_code = models.CharField(blank=False,null=False,verbose_name=u"编号")
    returner = models.ForeignKey(User,blank=False,null=False,verbose_name=u'退料人')
    inspector = models.ForeignKey(User,blank=True,null=True,verbose_name=u'检查员')
    keeper = models.ForeignKey(User,blank=True,null=True,verbose_name=u"库管员")

    def __unicode__(self):
        return str(self.form_code)

    class Meta:
        verbose_name=u'退库单'
        verbose_name_plural=u'退库单'

class BoardSteelMaterialReturnCardContent(models.Model):
    card_info = models.ForeignKey(CommonSteelMaterialReturnCardInfo,blank=False,null=False,verbose_name=u"退库单表头")
    status = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"状态")
    quantity = models.FloatField(blank=False,null=False,verbose_name=u"数量")
    weight = models.FloatField(blank=False,null=False,verbose_name=u"重量")
    weight_management =models.IntegerField(choices=WEIGHT_MANAGEMENT,blank=False,null=False,verbose_name=u"重量单位")
    remark = models.CharField(max_length=100,blank=True,null=True,verbose_name=u"备注")

    def __unicode__(self):
        return str(card_info)

    class Meta:
        verbose_name=u"板材退库单"
        verbose_name_plural=u"板材退库单"

class BarSteelMaterialReturnCardContent(models.Model):
    card_info = models.ForeignKey(CommonSteelMaterialReturnCardInfo,blank=False,null=False,verbose_name=u"退库单表头")
    status = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"状态")
    quantity = models.FloatField(blank=False,null=False,verbose_name=u"数量")
    length = models.FloatField(blank=False,null=False,verbose_name=u"长度")
    length_management =models.IntegerField(choices=LENGHT_MANAGEMENT,blank=False,null=False,verbose_name=u"长度单位")
    remark = models.CharField(max_length=100,blank=True,null=True,verbose_name=u"备注")

    def __unicode__(self):
        return str(card_info)

    class Meta:
        verbose_name=u"型材退库单"
        verbose_name_plural=u"板材退库单"



