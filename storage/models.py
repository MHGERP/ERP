#coding=UTF-8
import datetime
from const import *
from django.db import models
from django.db.models import Sum
from const.models import WorkOrder,Materiel,SubWorkOrder
from production.models import SubMateriel
from django.contrib.auth.models import User
from users.models import UserInfo,Group
from django.utils import timezone
from purchasing.models import BidForm,MaterielCopy
from random import randint
from django.conf import settings
# Create your models here.

class StorageEntryBaseA(models.Model):
    change_code = models.CharField(verbose_name=u"修改号",max_length=20,blank=True,null=True)
    sample_report = models.CharField(verbose_name=u"样表",max_length=20,blank=True,null=True)
    entry_code = models.CharField(verbose_name=u"单据编号",max_length=20,unique=True)
    source  = models.CharField(verbose_name=u"货物来源",max_length=20,blank=True,null=True)
    inspection_record = models.CharField(verbose_name=u"检查记录表编号",max_length=20,blank=True,null=True)
    remark = models.CharField(verbose_name=u"备注",max_length=200,blank=True,null=True)
    entry_time = models.DateField(verbose_name=u"入库时间",null=True,auto_now_add=True)

    class Meta:
        verbose_name = u"入库单A"
        verbose_name_plural = u"入库单A"
        abstract = True
    def __unicode__(self):
        return '%s' % self.entry_code

class StorageEntryItemBaseA(models.Model):
    materiel = models.ForeignKey(Materiel,verbose_name=u"材料")
    schematic_index = models.CharField(verbose_name=u"标准号或图号",max_length=50,blank=True,null=True)
    specification = models.CharField(verbose_name=u"名称及规格",max_length=20,blank=True,null=True)
    material_mark = models.CharField(verbose_name=u"材料牌号",max_length=20,blank=True,null=True)
    batch_number = models.CharField(verbose_name=u"炉批号",max_length=20,blank=True,null=True)
    tag_number = models.CharField(verbose_name=u"标记号",max_length=20,blank=True,null=True)
    unit =  models.CharField(verbose_name=u"单位",max_length=20,blank=True,null=True)
    number = models.IntegerField(verbose_name=u"数量",default=0)

    class Meta:
        verbose_name = u"入库单A材料"
        verbose_name_plural = u"入库单A材料"
        abstract = True
    def __unicode__(self):
        return '%s(%s)' % (self.specification,self.materiel.order)

class StorageEntryBaseB(models.Model):
    work_order = models.CharField(verbose_name=u"工作令",max_length=100)
    entry_time = models.DateField(verbose_name="日期",auto_now=True)
    entry_code = models.CharField(verbose_name=u"单据编号",max_length=20,unique=True)

    class Meta:
        verbose_name = u"入库单B"
        verbose_name_plural = u"入库单B"
        abstract = True
    def __unicode__(self):
        return '%s' % self.entry_code

class StorageEntryItemBaseB(models.Model):
    materiel = models.ForeignKey(Materiel,verbose_name=u"材料")
    texture = models.CharField(verbose_name=u"材质",max_length=50,blank=True,null=True)
    specification = models.CharField(verbose_name=u"规格",max_length=20,blank=True,null=True)
    standard = models.CharField(verbose_name=u"标准",max_length=20,blank=True,null=True)
    material_number = models.CharField(verbose_name=u"材质编号",max_length=20,blank=True,null=True)
    status = models.CharField(verbose_name=u"状态",max_length=20,blank=True,null=True)
    unit =  models.CharField(verbose_name=u"单位",max_length=20,blank=True,null=True)
    number = models.IntegerField(verbose_name=u"数量",default=0)
    remark =  models.CharField(verbose_name=u"备注",max_length=50,blank=True,null=True)

    class Meta:
        verbose_name = u"入库单B材料"
        verbose_name_plural = u"入库单B材料"
        abstract = True
    def __unicode__(self):
        return '%s(%s)' % (self.name,self.materiel.order)

class ApplyCardBase(models.Model):
    change_code = models.CharField(verbose_name=u"修改号",max_length=20,blank=True,null=True)
    sample_report = models.CharField(verbose_name=u"样表",max_length=20,blank=True,null=True)
    entry_code = models.CharField(verbose_name=u"编号",max_length=20,unique=True)
    work_order = models.ForeignKey(SubWorkOrder,verbose_name=u"工作令")
    create_time = models.DateField(verbose_name=u"日期")
    department = models.CharField(verbose_name = u"领用单位",max_length=20)
    class Meta:
        verbose_name = u"领用卡"
        verbose_name_plural = u"领用卡"
        abstract = True

class WeldMaterialEntry(models.Model):
    create_time = models.DateField(blank=False, null=True,auto_now_add=True,verbose_name=u"入库时间")
    purchaser =  models.ForeignKey(User,blank=True,null=True,verbose_name=u"采购员",related_name = "weldentry_purchaser")
    inspector = models.ForeignKey(User,blank=True,null=True,verbose_name=u"检验员",related_name = "weldentry_inspector")
    keeper = models.ForeignKey(User,blank=True,null=True,verbose_name=u"库管员" , related_name = "weldentry_keeper")
    entry_code = models.CharField(blank = False,null=True ,max_length = 20, verbose_name = u"单据编号",unique = True)
    entry_status = models.IntegerField(choices=ENTRYSTATUS_CHOICES,default=ENTRYSTATUS_CHOICES_PUCAHSER,verbose_name=u"入库单状态")
    class Meta:
        verbose_name = u"焊材入库单"
        verbose_name_plural = u"焊材入库单"

    def __unicode__(self):
        return '%s' % self.entry_code

    def auth_status(self,status):
        return self.entry_status == status

class WeldMaterialEntryItems(models.Model):
    material = models.ForeignKey(MaterielCopy,blank = True , null = True , verbose_name = u"材料")
    remark = models.CharField(max_length = 100, blank = True , default="" , verbose_name = u"备注")
    production_date = models.DateField( blank = True ,null = True, verbose_name = u"出厂日期")
    factory = models.CharField(max_length = 100, blank = True , verbose_name = u"厂家")
    price = models.FloatField( blank = True , null = True,verbose_name = u"单价")
    total_weight = models.FloatField( blank = True , default= 0,verbose_name = u"公斤数")
    single_weight = models.FloatField( blank = True , default = 0,verbose_name = u"单件重量")
    count = models.FloatField( blank = True , default = 0,verbose_name = u"件数")
    entry = models.ForeignKey(WeldMaterialEntry,verbose_name = u"焊材入库单")
    material_charge_number = models.CharField(max_length = 20, blank = True , verbose_name = u"材料批号")
    material_code = models.CharField(max_length = 20, blank = True , verbose_name = u"材质编号")
    material_mark = models.CharField(max_length = 50, blank = True , verbose_name = u"牌号")
    model_number = models.CharField(max_length = 50, blank = True , verbose_name = u"型号")
    specification = models.CharField(max_length = 20, blank = True , verbose_name = u"规格")
    class Meta:
        verbose_name = u"焊材入库材料"
        verbose_name_plural = u"焊材入库材料"
    def __unicode__(self):
        return '%s(%s)' % (self.material_mark, self.entry)

class WeldStoreListManager(models.Manager):
    def qualified_set(self):
        return self.filter(deadline__gte = datetime.date.today())

class WeldStoreList(models.Model):
    deadline = models.DateField(verbose_name=u"最后期限",null = True)
    count = models.FloatField(verbose_name=u"数量",default=0)
    entry_item = models.ForeignKey(WeldMaterialEntryItems,verbose_name = u"焊材入库单材料")
    item_status = models.IntegerField(choices=WELD_ITEM_STATUS_CHOICES,default=0,verbose_name=u"材料状态",blank=False)
    objects = WeldStoreListManager()
    class Meta:
        verbose_name = u"焊材库存清单"
        verbose_name_plural = u"焊材库存清单"

    def __unicode__(self):
        return "%s(%s)" % (self.entry_item.specification,self.entry_time)

    def save(self,*args,**kwargs):
        if self.count > 0 and self.item_status == ITEM_STATUS_SPENT:
            self.item_status = ITEM_STATUS_NORMAL #退库更新状态
        if self.item_status == ITEM_STATUS_NORMAL and self.count == 0:
            self.item_status = ITEM_STATUS_SPENT #领用更新状态
        super(WeldStoreList,self).save(*args,**kwargs)

class ApplyCardItemBase(models.Model):
    schematic_index = models.CharField(verbose_name=u"零件图/标准",max_length=50,blank=True,null=True)
    specification = models.CharField(verbose_name=u"名称及规格",max_length=20,blank=True,null=True)
    material_mark = models.CharField(verbose_name=u"材料牌号",max_length=20,blank=True,null=True)
    tag_number = models.CharField(verbose_name=u"标记号",max_length=20,blank=True,null=True)
    unit =  models.CharField(verbose_name=u"单位",max_length=20,blank=True,null=True)
    number = models.IntegerField(verbose_name=u"数量",default=0)
    remark = models.CharField(verbose_name=u"备注",max_length=50,blank=True,null=True)
    is_past = models.BooleanField(verbose_name=u"是否处理",default=False)
    class Meta:
        verbose_name = u"领用单物品"
        verbose_name_plural = u"领用单物品"
        abstract = True

class WeldingMaterialApplyCard(models.Model):
    department = models.CharField(verbose_name=u'领用单位',max_length=20,blank=False)
    applycard_code = models.CharField(verbose_name=u'编号',max_length=20,blank=False,unique=True)
    create_time=models.DateField(verbose_name=u'填写时间',auto_now_add=True)
    work_order=models.ForeignKey(SubWorkOrder,verbose_name=u'工作令',blank=False)
    weld_bead_number=models.CharField(verbose_name=u'焊缝编号',max_length=20,blank=False)
    material_mark=models.CharField(verbose_name=u'焊材牌号',max_length=50,blank=False)
    model_number=models.CharField(verbose_name=u'型号',max_length=50,blank=True)
    specification=models.CharField(verbose_name=u'规格',max_length=20,blank=False)
    apply_weight=models.FloatField(verbose_name=u'领用重量',blank=False,null=True)
    apply_count=models.FloatField(verbose_name=u'领用数量',blank=True,null=True)
    material_code=models.CharField(verbose_name=u'材质标记',max_length=20,blank=True,null=True)
    actual_weight=models.FloatField(verbose_name=u'实发重量',blank=False,null=True)
    actual_count=models.FloatField(verbose_name=u'实发数量',blank=True,null=True)
    applicant=models.ForeignKey(User,verbose_name=u'领用人',blank=True,null=True,related_name="weld_applicant")
    auditor=models.ForeignKey(User,verbose_name=u'审核人',blank=True,null=True,related_name="weld_auditor")
    inspector=models.ForeignKey(User,verbose_name=u'检查员',blank=True,null=True,related_name="weld_inspector")
    keeper = models.ForeignKey(User,verbose_name=u'发料人',blank=True,null=True,related_name="weld_keeper")
    status=models.IntegerField(verbose_name=u'领用状态',choices=APPLYCARD_STATUS_CHOICES,default=APPLYCARD_APPLICANT,blank=False)
    remark = models.CharField(verbose_name=u"备注",max_length=100,blank=True,null=True)
    storelist = models.ForeignKey(WeldStoreList,blank=True,null = True,verbose_name=u'库存材料')
    def __unicode__(self):
        return str(self.applycard_code)


    class Meta:
        verbose_name=u'焊材领用卡'
        verbose_name_plural=u'焊材领用卡'


class StoreRoom(models.Model):
    name = models.CharField(max_length=20,verbose_name=u"库房名称",blank = False)
    position = models.CharField(max_length=50,verbose_name=u"位置",blank = True)
    material_type = models.IntegerField(choices=STOREROOM_CHOICES,blank=False,null=False,default=STOREROOM_CHOICES_WELD,verbose_name=u"材料类型")

    def __unicode__(self):
        return "%s"  % self.name

    class Meta:
        verbose_name = u"库房"
        verbose_name_plural = u"库房"

class WeldingMaterialHumitureRecord(models.Model):
    storeMan = models.ForeignKey(User,verbose_name=u'库管员',blank=False,related_name="humitureStoreMan")
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
        verbose_name_plural=u'焊材库温湿度记录卡'

class WeldingMaterialBakeRecord(models.Model):
    date = models.DateField(verbose_name = u"日期",blank=False,null=True)
    index = models.CharField(verbose_name=u'编号',max_length=50,unique = True)
    standardnum = models.CharField(verbose_name=u'标准号',max_length=50,blank=True)
    size = models.CharField(verbose_name=u'规格',max_length=50,blank=True)
    classnum = models.CharField(verbose_name=u'牌号',max_length=50,blank=False)
    heatnum = models.CharField(verbose_name=u'炉批号',max_length=50,blank=False)
    codedmark = models.CharField(verbose_name=u'编码标记',max_length=50,blank=True)
    quantity = models.FloatField(verbose_name=u'数量',default = 0,blank=True)
    intoheattime = models.DateTimeField(verbose_name=u'进炉时间',blank=True,null=True)
    bakingtemp = models.FloatField(verbose_name=u'烘焙温度',default = 0,blank=True)
    timefortemp = models.DateTimeField(verbose_name=u'到达温度时间',blank=True,null=True)
    tempfalltime = models.DateTimeField(verbose_name=u'降温时间',blank=True,null=True)
    timeforremainheat = models.DateTimeField(verbose_name=u'进保湿炉时间',blank=True,null=True)
    keepheattemp = models.FloatField(verbose_name=u'保温温度',default = 0,blank=True)
    usetime = models.DateTimeField(verbose_name=u'领用时间',blank=True,null=True)
    storeMan = models.ForeignKey(User,verbose_name=u'库管员',related_name="weldbake_storeMan",blank=True)
    weldengineer = models.ForeignKey(User,verbose_name=u'焊接工程师',related_name="weldbake_engineer",blank=True,null=True)
    remark = models.CharField(verbose_name=u'备注', max_length=1000,blank=True)
    def __unicode__(self):
        return str(self.index)

    class Meta:
        verbose_name=u'焊材烘焙记录卡'
        verbose_name_plural=u'焊材烘焙记录卡'

class SteelMaterialEntry(models.Model):
    material_source = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'货物来源')
    entry_code = models.CharField(max_length=20,blank=False,null=False,verbose_name="入库单编号")
    purchaser =  models.ForeignKey(User,blank=True,null=True,related_name="steel_entry_purchaser",verbose_name=u"采购员")
    inspector = models.ForeignKey(User,blank=True,null=True,related_name="steel_entry_inspector",verbose_name=u"检验员",)
    keeper = models.ForeignKey(User,blank=True,null=True,related_name = "steel_entry_keeper",verbose_name=u"库管员" ,)
    create_time = models.DateField(blank=False,null=True,auto_now_add=True,verbose_name=u"入库时间")
    entry_status = models.IntegerField(choices=ENTRYSTATUS_CHOICES,default=ENTRYSTATUS_CHOICES_PUCAHSER,verbose_name=u"入库单状态")
    steel_type = models.IntegerField(choices = STEEL_TYPE,default=BOARD_STEEL,verbose_name=u"入库单类型")
    remark = models.CharField(verbose_name=u'备注', max_length=100,blank=True,default="")
    def __unicode__(self):
        return str(self.entry_code)

    class Meta:
        verbose_name=u"钢材入库单"
        verbose_name_plural=u"钢材入库单"

class SteelMaterialEntryItems(models.Model):
    specification = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'名称及规格')
    batch_number = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'炉批号')
    material_mark = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'材料牌号')
    material_code = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'标记号')
    weight = models.FloatField(blank=False,null=False,verbose_name=u"重量")
    unit = models.CharField(blank=True,null=True,max_length=20,verbose_name=u"单位")
    work_order = models.ManyToManyField(SubWorkOrder,blank=False,null=False,verbose_name=u'工作令')
    count = models.IntegerField(blank=False,null=False,verbose_name=u"数量")
    length = models.FloatField(blank=True,null=True,verbose_name=u"长度")
    entry = models.ForeignKey(SteelMaterialEntry,verbose_name=u"钢材入库单")
    schematic_index = models.CharField(max_length=50,verbose_name=u"标准号或图号")
    material = models.ForeignKey(MaterielCopy,null=True,blank=True,verbose_name=u"物料")
    def __unicode__(self):
        return "%s"% self.specification

    def show_workorder(self):
        workorder_set = self.work_order.all()
        work_order_list = []
        for order in workorder_set:
            work_order_list.append(order.__unicode__())
        work_order_str = ','.join(work_order_list)
        return work_order_str

    class Meta:
        verbose_name=u'钢材入库材料'
        verbose_name_plural=u'钢材入库材料'


class SteelMaterialStoreList(models.Model):
    entry_item = models.ForeignKey( SteelMaterialEntryItems , verbose_name=u"钢材入库材料")
    specification = models.CharField(max_length=50,blank=False,null=False,verbose_name=u'名称及规格')
    steel_type = models.IntegerField(choices = STEEL_TYPE,verbose_name=u"材料类型")
    length = models.FloatField(blank=True,null=True,verbose_name=u"长度")
    count = models.IntegerField(blank=False,null=False,verbose_name=u"数量")
    weight = models.FloatField(blank=True,null=True,verbose_name=u"重量")
    return_time = models.IntegerField(default=0,verbose_name=u'退库次数')
    store_room = models.ForeignKey(StoreRoom,blank=True,null=True,verbose_name=u'库房位置')
    refund = models.IntegerField(verbose_name=u"退库单",blank=True,null=True)
    class Meta:
        verbose_name=u'钢材库存材料'
        verbose_name_plural=u'钢材库存材料'
    def __unicode__(self):
        return "%s" % self.specification


class SteelMaterialApplyCard(models.Model):
    department = models.CharField(max_length=50,blank=False,null=False,verbose_name=u"领用单位")
    create_time = models.DateField(blank=False,null=False,auto_now_add=True,verbose_name=u"日期")
    applycard_code = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"编号")
    applicant = models.ForeignKey(User,blank=True,null=True,verbose_name=u'领料人',related_name="steel_apply_applicanter")
    auditor = models.ForeignKey(User,blank=True,null=True,verbose_name=u'审核人',related_name="steel_apply_auditor")
    inspector = models.ForeignKey(User,blank=True,null=True,verbose_name=u'检查员',related_name="steel_apply_inspector")
    keeper = models.ForeignKey(User,blank=True,null=True,verbose_name=u"发料人",related_name="steel_apply_keeper")
    remark = models.CharField(blank=True,null=True,max_length=100,verbose_name=u'备注')
    status=models.IntegerField(verbose_name=u'领用状态',choices=APPLYCARD_STATUS_CHOICES,default=APPLYCARD_APPLICANT,blank=False)
    def __unicode__(self):
        return self.applycard_code

    class Meta:
        verbose_name=u"钢材领用单"
        verbose_name_plural=u"钢材领用单"


class SteelMaterialApplyCardItems(models.Model):
    storelist = models.ForeignKey(SteelMaterialStoreList,blank=True,null=True,verbose_name=u"库存材料")
    apply_card = models.ForeignKey(SteelMaterialApplyCard,blank=False,null=False,verbose_name=u"钢材领用单")
    count = models.IntegerField(blank=False,null=False,verbose_name=u"申请数量")
    material_mark = models.CharField(max_length=20,blank=False,null=True,verbose_name=u'钢号')
    material_code = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'材质编号')
    component = models.CharField(max_length=100,blank=True,null=True,verbose_name=u"零件编号")
    work_order=models.ForeignKey(SubWorkOrder,blank=False,null=False,verbose_name=u"工作令")
    submateriel = models.ForeignKey(SubMateriel, null=True, verbose_name = u"工作票")
    specification = models.CharField(max_length=50,blank=False,null=False,verbose_name=u'规格')
    def __unicode__(self):
        return "%s" % self.material_mark

    class Meta:
        verbose_name=u"钢材领用单材料"
        verbose_name_plural=u"钢材领用单材料"

class SteelMaterialRefundCard(models.Model):
    work_order=models.ForeignKey(SubWorkOrder,blank=False,null=False,verbose_name=u"工作令")
    create_time = models.DateField(blank=False,null=False,auto_now_add=True,verbose_name=u"日期")
    refund_code = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"编号")
    refunder = models.ForeignKey(User,blank=False,null=True,verbose_name=u'退料人',related_name="steel_refund_refunder")
    inspector = models.ForeignKey(User,blank=True,null=True,verbose_name=u'检查员',related_name="steel_refund_inspector")
    keeper = models.ForeignKey(User,blank=True,null=True,verbose_name=u"库管员",related_name="steel_refund_keeper")
    status = models.IntegerField(default=REFUNDSTATUS_STEEL_CHOICES_REFUNDER,choices=REFUNDSTATUS_STEEL_CHOICES,verbose_name=u"退库单状态")
    steel_type = models.IntegerField(choices=STEEL_TYPE,default=BOARD_STEEL,verbose_name=u'钢材类型')#1:bar 0:board
    applycard = models.ForeignKey(SteelMaterialApplyCard,blank=True,null=True,verbose_name=u"领用单")
    def __unicode__(self):
        return str(self.refund_code)

    class Meta:
        verbose_name=u'钢材退库单'
        verbose_name_plural=u'钢材退库单'

class BoardSteelMaterialRefundItems(models.Model):
    applyitem = models.ForeignKey(SteelMaterialApplyCardItems,verbose_name=u"申请材料")
    name = models.CharField(max_length=20,verbose_name=u"名称")
    card_info = models.OneToOneField(SteelMaterialRefundCard,blank=False,null=False,verbose_name=u"退库单表头")
    status = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"状态")
    specification = models.CharField(max_length=50,blank=True,null=True,verbose_name=u'名称及规格')
    count = models.IntegerField(blank=False,null=False,verbose_name=u"数量")
    weight = models.FloatField(blank=True,null=True,verbose_name=u"重量")
    graph = models.FileField(upload_to=settings.PROCESS_FILE_PATH+"/storage",null=True,verbose_name=u"套料图")
    remark = models.CharField(max_length=100,default="",blank=True,null=True,verbose_name=u"备注")

    def __unicode__(self):
        return str(self.card_info)

    class Meta:
        verbose_name=u"板材退库材料"
        verbose_name_plural=u"板材退库单材料"

class BarSteelMaterialRefundItems(models.Model):
    applyitem = models.ForeignKey(SteelMaterialApplyCardItems,verbose_name=u'申请材料')
    name = models.CharField(max_length=20,verbose_name=u"名称")
    card_info = models.ForeignKey(SteelMaterialRefundCard,blank=False,null=False,verbose_name=u"退库单表头")
    status = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"状态")
    specification = models.CharField(max_length=50,blank=True,null=True,verbose_name=u'名称及规格')
    count = models.IntegerField(blank=False,null=False,verbose_name=u"数量")
    weight = models.FloatField(blank=True,null=True,verbose_name=u"重量")
    length = models.FloatField(null=True,verbose_name=u"退库长度")
    remark = models.CharField(default="", max_length=100,blank=True,null=True,verbose_name=u"备注")

    def __unicode__(self):
        return str(self.card_info)

    class Meta:
        verbose_name=u"型材退库单材料"
        verbose_name_plural=u"型材退库单材料"

class WeldRefund(models.Model):
    department  = models.CharField(verbose_name=u"领用单位",max_length=20,blank=False)
    refund_code = models.CharField(verbose_name=u"编号",max_length=20,blank=False)
    create_time = models.DateField(blank=False,null=True,verbose_name=u"日期",auto_now_add = True)
    apply_card = models.OneToOneField(WeldingMaterialApplyCard,blank=False,verbose_name=u"领用单编号")
    refund_weight = models.FloatField(null=True,blank=False,verbose_name=u"退库量（重量）")
    refund_count = models.FloatField(null=True,blank=True,verbose_name=u"退库量（数量）")
    refund_status = models.CharField(max_length=20,blank=True,verbose_name=u"退库状态",default="")
    status = models.IntegerField(default=REFUNDSTATUS_CHOICES_REFUNDER,choices=REFUNDSTATUS_CHOICES,verbose_name=u"退库单状态")
    refunder =  models.ForeignKey(User,verbose_name=u"退库人",null=True,blank=True,related_name = "weldrefund_refunder")
    keeper = models.ForeignKey(User,verbose_name=u"库管人",null=True,blank=True,related_name = "weldrefund_keeper")

    class Meta:
        verbose_name = u"焊接材料退库卡"
        verbose_name_plural = u"焊接材料退库卡"

    def __unicode__(self):
        return '%s' % self.apply_card


class AuxiliaryToolEntry(models.Model):
    create_time = models.DateField(verbose_name=u'入库时间', auto_now_add=True)
    purchaser = models.ForeignKey(User, blank=True, null=True,
                                  verbose_name=u'采购员', related_name='au_purchaser')
    inspector = models.ForeignKey(User, blank=True, null=True,
                                  verbose_name=u'检验员', related_name='au_inspector')
    keeper = models.ForeignKey(User, blank=True, null=True,
                               verbose_name=u'库管员', related_name='au_keeper')
    entry_code = models.CharField(blank=False, null=True, max_length=20,
                             verbose_name=u'编号', unique=True)
    entry_status = models.IntegerField(choices=ENTRYSTATUS_CHOICES,
                                 default=ENTRYSTATUS_CHOICES_PUCAHSER,
                                 verbose_name=u'入库单状态')

    class Meta:
        verbose_name = u'辅助材料入库单'
        verbose_name_plural = u'辅助材料入库单'

    def __unicode__(self):
        return '%s' % self.entry_code

class AuxiliaryToolEntryItems(models.Model):
    name = models.CharField(blank=False, max_length=50,verbose_name=u"名称")
    specification = models.CharField(blank=True,max_length=50,verbose_name=u"规格")
    count = models.FloatField(verbose_name=u'入库数量',blank=False)
    unit = models.CharField(blank=True,max_length=50,verbose_name=u"单位")
    factory = models.CharField(blank=True, null=True, max_length=100,verbose_name=u"厂家")
    supplier = models.CharField(blank=True, null=True, max_length=100,verbose_name=u"供货商")
    remark = models.CharField(blank=True, null=True,default="", max_length=100,verbose_name=u"备注")
    entry =models.ForeignKey(AuxiliaryToolEntry,verbose_name=u'辅助工具入库单')

    class Meta:
        verbose_name=u'辅助材料入库材料'
        verbose_name_plural=u'辅助材料入库材料'

    def __unicode__(self):
        return u'%s(%s)'%(self.name,self.specification)

class AuxiliaryToolStoreList(models.Model):
    entry_item = models.ForeignKey(AuxiliaryToolEntryItems,verbose_name=u"辅助工具入库材料")
    count = models.FloatField(verbose_name=u"数量",blank=True,null=True)
    item_status = models.IntegerField(choices=WELD_ITEM_STATUS_CHOICES,default=0,verbose_name=u"材料状态",blank=False)
    class Meta:
        verbose_name=u'辅助库存材料'
        verbose_name_plural=u'辅助库存材料'

    def __unicode__(self):
        return "%s" % self.entry_item.name

    def save(self,*args,**kwargs):
        if self.count > 0 and self.item_status == ITEM_STATUS_SPENT:
            self.item_status = ITEM_STATUS_NORMAL #退库更新状态
        if self.item_status == ITEM_STATUS_NORMAL and self.count == 0:
            self.item_status = ITEM_STATUS_SPENT #领用更新状态
        super(AuxiliaryToolStoreList,self).save(*args,**kwargs)

class AuxiliaryToolApplyCard(models.Model):
    create_time=models.DateField(verbose_name=u'申请时间',auto_now_add=True)
    department = models.CharField(verbose_name=u"领用单位",max_length=50,blank=True,null=True)
    applycard_code = models.CharField(verbose_name=u"料单编号",max_length=20,blank=True,null=True)
    apply_storelist=models.ForeignKey(AuxiliaryToolStoreList,verbose_name=u'申请材料',blank=False,null=True,related_name="auap_apply_storelist")
    apply_count=models.IntegerField(verbose_name=u'申请数量',blank=False)
    storelist = models.ForeignKey(AuxiliaryToolStoreList,verbose_name=u'实发材料',null=True,blank=True,related_name="auap_actual_storelist")
    actual_count=models.IntegerField(verbose_name=u'实发数量',null=True,blank=True)
    status=models.IntegerField(verbose_name=u'领用单状态',choices=AUXILIARY_TOOL_APPLY_CARD_STATUS,default=AUXILIARY_TOOL_APPLY_CARD_APPLICANT)
    applicant=models.ForeignKey(User,verbose_name=u'领料',blank=True,null=True,related_name="at_applicants")
    auditor = models.ForeignKey(User,verbose_name=u"主管",null=True,blank=True,related_name="at_auditor")
    keeper=models.ForeignKey(User,verbose_name=u'发料',blank=True,null=True,related_name="at_keeper")
    remark=models.TextField(verbose_name=u'备注',default="",blank=True,null=True)

    class Meta:
        verbose_name=u'辅助材料领用卡'
        verbose_name_plural=u'辅助材料领用卡'
    def __unicode__(self):
        return "%s" % self.applycard_code

class WeldStoreThread(models.Model):
    specification = models.CharField(max_length=50,verbose_name=u"规格")
    count = models.FloatField(verbose_name=u"数量")
    type=  models.CharField(verbose_name=u"材料种类",choices = MATERIAL_CATEGORY_CHOICES,max_length=20)
    class Meta:
        verbose_name = u"库存安全量"
        verbose_name_plural = u"库存安全量"
    def __unicode__(self):
        return '%s' % self.specification

class OutsideStandardEntry(models.Model):
    purchaser =  models.ForeignKey(User,blank=True,null=True,verbose_name=u"采购员",related_name = "outside_entry_purchaser")
    inspector = models.ForeignKey(User,blank=True,null=True,verbose_name=u"检验员",related_name = "outside_entry_inspector")
    keeper = models.ForeignKey(User,blank=True,null=True,verbose_name=u"库管员" , related_name = "outside_entry_keeper")
    entry_status = models.IntegerField(choices=ENTRYSTATUS_CHOICES,default=ENTRYSTATUS_CHOICES_PUCAHSER,verbose_name=u"入库单状态")
    material_source = models.CharField(max_length=50,blank=True,null=True,verbose_name=u'货物来源')
    bidform_code = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'订购单编号')
    inspection_record = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'接收检查记录表')
    entry_code = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'编号')
    change_code = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'修改号')
    sample_report = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'样表')
    create_time = models.DateField(verbose_name=u"入库时间",null=True,auto_now_add=True)
    remark = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'备注')
    outsidebuy_type = models.IntegerField(choices=OUTSIDEBUY_TYPE,default=COOPERATION_OUTSIDEBUY,verbose_name=u"外购件类型")
    class Meta:
        verbose_name = u"外购件入库单"
        verbose_name_plural = u"外购件入库单"
    def __unicode__(self):
        return "%s" % self.entry_code

class OutsideStandardItems(models.Model):
    entry = models.ForeignKey(OutsideStandardEntry,verbose_name = u"入库单")
    materiel = models.ForeignKey(MaterielCopy,verbose_name=u"物料",null=True,blank=True)
    schematic_index = models.CharField(verbose_name=u"标准号或图号",max_length=50,blank=True,null=True)
    specification = models.CharField(verbose_name=u"名称及规格",max_length=50,blank=True,null=True)
    material_mark = models.CharField(verbose_name=u"材料牌号",max_length=50,blank=True,null=True)
    batch_number = models.CharField(verbose_name=u"炉批号",max_length=50,blank=True,null=True)
    material_code = models.CharField(verbose_name=u"标记号",max_length=20,blank=True,null=True)
    unit =  models.CharField(verbose_name=u"单位",max_length=20,blank=True,null=True)
    count = models.IntegerField(verbose_name=u"数量",default=0)
    weight = models.FloatField(verbose_name=u"净重",null=True,blank=True)
    heatnum = models.CharField(verbose_name=u"熔炼号",null=True,blank=True,max_length=50)
    remark = models.CharField(max_length=50,blank=True,null=True,verbose_name=u'备注')
    factory = models.CharField(max_length=50,blank=True,null=True,verbose_name=u'生产厂家')
    ticket_number = models.CharField(max_length=50,blank=True,null=True,verbose_name=u'票号')
    work_order=models.ForeignKey(SubWorkOrder,blank=False,null=False,verbose_name=u"工作令")
    class Meta:
        verbose_name = u"外购件入库材料"
        verbose_name_plural = u"外购件入库材料"
    def __unicode__(self):
        return '%s' % self.specification


class OutsideStorageList(models.Model):
    entry_item = models.OneToOneField(OutsideStandardItems,verbose_name=u"入库材料")
    count = models.IntegerField(verbose_name=u"数量",default=0)
    outsidebuy_type = models.IntegerField(choices=OUTSIDEBUY_TYPE,default=COOPERATION_OUTSIDEBUY,verbose_name=u"外购件类型")
    class Meta:
        verbose_name = u"外购件库存材料"
        verbose_name_plural = u"外购件库存材料"

    def __unicode__(self):
        return "%s" % self.entry_item.specification


class OutsideApplyCard(models.Model):
    applicant = models.ForeignKey(User,blank=True,null=True,verbose_name=u"领用人",related_name = "out_apply_applicant")
    auditor = models.ForeignKey(User,blank=True,null=True,verbose_name=u"审核人",related_name = "out_apply_auditor")
    inspector = models.ForeignKey(User,blank=True,null=True,verbose_name=u"检验员",related_name = "out_apply_inspector")
    keeper = models.ForeignKey(User,blank=True,null=True,verbose_name=u"库管员" , related_name = "out_apply_keeper")
    status = models.IntegerField(choices=APPLYCARD_STATUS_CHOICES,default=APPLYCARD_APPLICANT,verbose_name=u"领用单状态")
    change_code = models.CharField(verbose_name=u"修改号",max_length=50,blank=True,null=True)
    sample_report = models.CharField(verbose_name=u"样表",max_length=50,blank=True,null=True)
    applycard_code = models.CharField(verbose_name=u"编号",max_length=20)
    work_order = models.ForeignKey(SubWorkOrder,verbose_name=u"工作令")
    submateriel = models.ForeignKey(SubMateriel, null=True, verbose_name = u"工作票")
    create_time = models.DateField(verbose_name=u"日期",auto_now_add=True)
    department = models.CharField(verbose_name = u"领用单位",max_length=20,null=True,blank=True)

    class Meta:
        verbose_name = u"外购件领用单"
        verbose_name_plural = u"外购件领用单"
    def __unicode__(self):
        return self.applycard_code

class OutsideApplyCardItems(models.Model):
    apply_card = models.ForeignKey(OutsideApplyCard,verbose_name=u"领用单")
    storelist = models.ForeignKey(OutsideStorageList,verbose_name=u"外购件库存材料",null=True,blank=True)
    schematic_index = models.CharField(verbose_name=u"标准号或图号",max_length=50,blank=True,null=True)
    specification = models.CharField(verbose_name=u"名称及规格",max_length=50,blank=True,null=True)
    material_mark = models.CharField(verbose_name=u"材料牌号",max_length=50,blank=True,null=True)
    material_code = models.CharField(verbose_name=u"标记号",max_length=20,blank=True,null=True)
    unit =  models.CharField(verbose_name=u"单位",max_length=20,blank=True,null=True)
    count = models.IntegerField(verbose_name=u"数量",default=0)
    remark =  models.CharField(verbose_name=u"备注",max_length=50,blank=True,null=True)

    class Meta:
        verbose_name = u"外购件领用单材料"
        verbose_name_plural = u"外购件领用单材料"
    def __unicode__(self):
        return "%s" %  self.specification

class OutsideRefundCard(models.Model):
    refunder = models.ForeignKey(User,blank=True,null=True,verbose_name=u"退库人",related_name = "out_refund_refunder")
    keeper = models.ForeignKey(User,blank=True,null=True,verbose_name=u"库管员" , related_name = "out_refund_keeper")
    status = models.IntegerField(choices=REFUNDSTATUS_CHOICES,default=REFUNDSTATUS_STEEL_CHOICES_REFUNDER,verbose_name=u"退库单状态")
    applycard = models.ForeignKey(OutsideApplyCard,verbose_name=u"外购件领用单")
    refundcard_code = models.CharField(verbose_name=u"退库单编号",max_length=20)
    work_order = models.ForeignKey(SubWorkOrder,verbose_name=u"工作令")
    create_time = models.DateField(verbose_name=u"日期",auto_now_add=True)

    class Meta:
        verbose_name = u"外购件退库单"
        verbose_name_plural = u"外购件退库单"
    def __unicode__(self):
        return self.refundcard_code

class OutsideRefundCardItems(models.Model):
    refundcard = models.ForeignKey(OutsideRefundCard,verbose_name=u"退库单")
    applyitem = models.ForeignKey(OutsideApplyCardItems,verbose_name=u"领用材料")
    count = models.IntegerField(verbose_name=u"数量",default=0)
    remark =  models.CharField(verbose_name=u"备注",max_length=50,blank=True,null=True)

    class Meta:
        verbose_name = u"外购件退库单材料"
        verbose_name_plural = u"外购件退库单材料"
    def __unicode__(self):
        return "%s" %  self.applyitem.specification

class CardStatusStopRecord(models.Model):
    user  = models.ForeignKey(User,verbose_name="操作者")
    create_time = models.DateField(blank=False,null=True,verbose_name=u"日期",auto_now_add = True)
    card_type = models.CharField(max_length=20,verbose_name=u"单据类型")
    card_id = models.IntegerField(verbose_name=u"单据ID")
    remark = models.TextField(max_length=1000,verbose_name=u"原因")
    class Meta:
        verbose_name = u"单据终止记录"
        verbose_name_plural = u"单据终止记录"

    def __unicode__(self):
        return '%s' % self.card_type
