#coding=UTF-8
import datetime
from const import *
from django.db import models
from django.db.models import Sum
from const.models import WorkOrder,Materiel
from django.contrib.auth.models import User
from users.models import UserInfo,Group
from django.utils import timezone
from const import STORAGEDEPARTMENT_CHOICES,STORAGESTATUS_KEEPER,REFUNDSTATUS_CHOICES
from const import LENGHT_MANAGEMENT,WEIGHT_MANAGEMENT,AREA_MANAGEMENT,STEEL_TYPE,MATERIAL_TYPE
from purchasing.models import BidForm
from random import randint
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
    workorder = models.CharField(verbose_name=u"工作令",max_length=100)
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
    workorder = models.ForeignKey(WorkOrder,verbose_name=u"工作令")
    date = models.DateField(verbose_name=u"日期")
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
    entry_status = models.IntegerField(choices=ENTRYSTATUS_CHOICES,default=STORAGESTATUS_PURCHASER,verbose_name=u"入库单状态")
    class Meta:
        verbose_name = u"焊材入库单"
        verbose_name_plural = u"焊材入库单"

    def __unicode__(self):
        return '%s' % self.entry_code

    def auth_status(self,status):
        return self.entry_status == status

class WeldMaterialEntryItems(models.Model):
    material = models.ForeignKey(Materiel,blank = True , null = True , verbose_name = u"材料")
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
        return '%s(%s)' % (self.material.name, self.entry)

class WeldStoreListManager(models.Manager):
    def qualified_set(self):
        return self.filter(deadline__gte = datetime.date.today())

class WeldStoreList(models.Model):
    deadline = models.DateField(verbose_name=u"最后期限",null = True)
    inventory_count = models.FloatField(verbose_name=u"数量",default=0)
    entry_item = models.ForeignKey(WeldMaterialEntryItems,verbose_name = u"焊材入库单材料")
    item_status = models.IntegerField(choices=WELD_ITEM_STATUS_CHOICES,default=0,verbose_name=u"材料状态",blank=False)
    entry_time = models.DateField(verbose_name=u"入库时间",null = True)
    objects = WeldStoreListManager()
    class Meta:
        verbose_name = u"焊材库存清单"
        verbose_name_plural = u"焊材库存清单"

    def __unicode__(self):
        return "%s(%s)" % (self.entry_item.material.name,self.entry_time)

    def save(self,*args,**kwargs):
        if self.inventory_count > 0 and self.item_status == ITEM_STATUS_SPENT:
            self.item_status = ITEM_STATUS_NORMAL #退库更新状态
        if self.item_status == ITEM_STATUS_NORMAL and self. inventory_count == 0:
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
    workorder=models.ForeignKey(WorkOrder,verbose_name=u'工作令',blank=False)
    weld_bead_number=models.CharField(verbose_name=u'焊缝编号',max_length=20,blank=False)
    material_mark=models.CharField(verbose_name=u'焊材牌号',max_length=50,blank=False)
    model_number=models.CharField(verbose_name=u'型号',max_length=50,blank=True)
    specification=models.CharField(verbose_name=u'规格',max_length=20,blank=False)
    apply_weight=models.FloatField(verbose_name=u'领用重量',blank=False,null=True)
    apply_quantity=models.FloatField(verbose_name=u'领用数量',blank=True,null=True)
    material_code=models.CharField(verbose_name=u'材质标记',max_length=20,blank=True,null=True)
    actual_weight=models.FloatField(verbose_name=u'实发重量',blank=False,null=True)
    actual_quantity=models.FloatField(verbose_name=u'实发数量',blank=True,null=True)
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
    material_type = models.IntegerField(choices=MATERIAL_TYPE,blank=False,null=False,default=0,verbose_name=u"材料类型")

    def __unicode__(self):
        return "%s"  % self.name

    class Meta:
        verbose_name = u"库房"
        verbose_name_plural = u"库房"

class WeldingMaterialHumitureRecord(models.Model):
    storeRoom = models.ForeignKey(StoreRoom,verbose_name=u"库房")
    storeMan = models.ForeignKey(User,verbose_name=u'库管员',blank=False,related_name="humitureStoreMan")
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
    weldengineer = models.ForeignKey(User,verbose_name=u'焊接工程师',related_name="weldbake_engineer",blank=True)
    remark = models.CharField(verbose_name=u'备注', max_length=1000,blank=True)
    def __unicode__(self):
        return str(self.index)

    class Meta:
        verbose_name=u'焊材烘焙记录卡'
        verbose_name_plural=u'焊材烘焙记录卡'

class SteelMaterialEntry(models.Model):
    material_source = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'货物来源')
    entry_code = models.CharField(max_length=20,blank=False,null=False,verbose_name="入库单编号")
    purchaser =  models.ForeignKey(User,blank=False,null=False,related_name="steel_entry_purchaser",verbose_name=u"采购员")
    inspector = models.ForeignKey(User,blank=False,null=False,related_name="steel_entry_inspector",verbose_name=u"检验员",)
    keeper = models.ForeignKey(User,blank=False,null=False,related_name = "steel_entry_keeper",verbose_name=u"库管员" ,)
    create_time = models.DateField(blank=False,null=True,auto_now_add=True,verbose_name=u"入库时间")
    entry_status = models.IntegerField(choices=ENTRYSTATUS_CHOICES,default=STORAGESTATUS_PURCHASER,verbose_name=u"入库单状态")
    steel_type = models.IntegerField(choices = STEEL_TYPE,default=BOARD_STEEL,verbose_name=u"入库单类型")
    remark = models.CharField(verbose_name=u'备注', max_length=100,blank=True,default="")
    def __unicode__(self):
        return str(self.entry_code)

    class Meta:
        verbose_name=u"钢材入库单"
        verbose_name_plural=u"钢材入库单"

class SteelMaterialEntryItems(models.Model):
    name = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'材料名称')
    specification = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'规格')
    batch_number = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'炉号')
    lot_number = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'批号')
    materiel = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'材质')
    material_code = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'材质编号')
    weight = models.FloatField(blank=False,null=False,verbose_name=u"重量")
    unit = models.CharField(blank=True,null=True,max_length=20,verbose_name=u"单位")
    work_order = models.ManyToManyField(WorkOrder,blank=False,null=False,verbose_name=u'工作令')
    store_room = models.ForeignKey(StoreRoom,blank=False,null=False,verbose_name=u'库房位置')
    count = models.IntegerField(blank=False,null=False,verbose_name=u"数量")
    length = models.FloatField(blank=True,null=True,verbose_name=u"长度")
    entry = models.ForeignKey(SteelMaterialEntry,verbose_name=u"钢材入库单")

    def __unicode__(self):
        return "%s(%s)"%(self.name,self.specification)

    def show_workorder(self):
        workorder_set = self.work_order.all()
        work_order_list = []
        for order in workorder_set:
            work_order_list.append(order.order_index)
        work_order_str = ','.join(work_order_list)
        return work_order_str

    class Meta:
        verbose_name=u'钢材入库材料'
        verbose_name_plural=u'钢材入库材料'


class SteelMaterialStoreList(models.Model):
    entry_item = models.ForeignKey( SteelMaterialEntryItems , verbose_name=u"钢材入库材料")
    name = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'材料名称')
    specification = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'规格')
    steel_type = models.IntegerField(choices = STEEL_TYPE,verbose_name=u"材料类型")
    length = models.FloatField(blank=True,null=True,verbose_name=u"长度")
    count = models.IntegerField(blank=False,null=False,verbose_name=u"数量")
    weight = models.FloatField(blank=False,null=False,verbose_name=u"重量")
    return_time = models.IntegerField(default=0,verbose_name=u'退库次数')
    store_room = models.ForeignKey(StoreRoom,blank=False,null=False,verbose_name=u'库房位置')
    class Meta:
        verbose_name=u'钢材库存材料'
        verbose_name_plural=u'钢材库存材料'
    def __unicode__(self):
        return "%s" % self.name

"""
class CommonSteelMaterialApplyCardInfo(models.Model):
    department = models.CharField(max_length=50,blank=False,null=False,verbose_name=u"领用单位")
    work_order=models.ForeignKey(WorkOrder,blank=False,null=False,verbose_name=u"工作令")
    date = models.DateField(blank=False,null=False,auto_now_add=True,verbose_name=u"日期")
    form_code = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"编号")
    applicant = models.ForeignKey(User,blank=False,null=False,verbose_name=u'退料人',related_name="Steel_applicanter")
    inspector = models.ForeignKey(User,blank=True,null=True,verbose_name=u'检查员',related_name="steel_apply_inspector")
    keeper = models.ForeignKey(User,blank=True,null=True,verbose_name=u"库管员",related_name="steel_apply_keeper")
    steel_type = models.IntegerField(choices=STEEL_TYPE,default=0,verbose_name=u'钢材类型')
    apply_confirm = models.BooleanField(blank=False,null=False,default=False,verbose_name=u"出库确认")
    remarkment = models.CharField(blank=True,null=True,max_length=100,verbose_name=u'备注')

    def __unicode__(self):
        return self.form_code

    class Meta:
        verbose_name=u"钢材领用单"
        verbose_name_plural=u"钢材领用单"
class BoardSteelMaterialApplyCardContent(models.Model):
    steel_material = models.ForeignKey(SteelMaterial,blank=False,null=False,verbose_name=u"材料信息")
    card_info = models.ForeignKey(CommonSteelMaterialApplyCardInfo,blank=False,null=False,verbose_name=u"领用单表头")
    status = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"状态")
    quantity = models.IntegerField(blank=False,null=False,verbose_name=u"数量")
    weight = models.FloatField(blank=False,null=False,verbose_name=u"重量")
    weight_management =models.IntegerField(choices=WEIGHT_MANAGEMENT,blank=False,null=False,verbose_name=u"重量单位")
    graph = models.CharField(max_length=100,blank=False,null=False,verbose_name=u"套料图")
    remark = models.CharField(max_length=100,blank=True,null=True,verbose_name=u"备注")

    def __unicode__(self):
        return str(self.card_info)

    class Meta:
        verbose_name=u"板材领用单详细信息"
        verbose_name_plural=u"板材领用单详细信息"

class BarSteelMaterialApplyCardContent(models.Model):
    steel_material = models.ForeignKey(SteelMaterial,blank=False,null=False,verbose_name=u'材料信息')
    card_info = models.ForeignKey(CommonSteelMaterialApplyCardInfo,blank=False,null=False,verbose_name=u"领用单表头")
    status = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"状态")
    quantity = models.IntegerField(blank=False,null=False,verbose_name=u"数量")
    length = models.FloatField(blank=False,null=False,verbose_name=u"长度")
    length_management =models.IntegerField(choices=LENGHT_MANAGEMENT,blank=False,null=False,verbose_name=u"长度单位")
    remark = models.CharField(max_length=100,blank=True,null=True,verbose_name=u"备注")

    def __unicode__(self):
        return str(self.card_info)

    class Meta:
        verbose_name=u"型材领用单详细信息"
        verbose_name_plural=u"型材领用单详细信息"




class BoardSteelMaterialLedger(models.Model):
    material_info = models.OneToOneField(SteelMaterial,blank=False,null=False,verbose_name="钢材信息")
    quantity = models.IntegerField(blank=False,null=False,verbose_name=u'钢板数量')
    weight = models.FloatField(blank=False,null=False,verbose_name=u'钢板重量',default=0)
    #weight_management = models.IntegerField(choices=WEIGHT_MANAGEMENT,default=0,blank=False,null=False,verbose_name=u'重量单位')
    area = models.FloatField(blank=False,null=False,verbose_name=u'钢板面积',default=0)
    area_management = models.IntegerField(choices=AREA_MANAGEMENT,default=0,blank=False,null=False,verbose_name=u'面积单位')
    slice_cad = models.CharField(max_length=50,blank=True,null=True,verbose_name=u'套料图')

    def __unicode__(self):
        return "%s(%s)"%(self.material_info.name,self.material_info.specifications)

    class Meta:
        verbose_name=u'板材台账'
        verbose_name_plural=u'板材台账'

class BarSteelMaterialLedger(models.Model):
    material_info = models.OneToOneField(SteelMaterial,blank=False,null=False,verbose_name=u"钢材信息")
    quantity = models.IntegerField(blank=False,null=False,verbose_name=u'型材数量')
    length = models.FloatField(blank=True,null=True,verbose_name=u"长度",default=0)
    length_management = models.IntegerField(choices=LENGHT_MANAGEMENT,default=0,verbose_name=u"长度单位")

    def __unicode__(self):
        return "%s(%s)"%(self.material_info.name,self.material_info.specifications)

    class Meta:
        verbose_name=u'型材台账'
        verbose_name_plural=u'型材台账'

class CommonSteelMaterialReturnCardInfo(models.Model):
    work_order=models.ForeignKey(WorkOrder,blank=False,null=False,verbose_name=u"工作令")
    date = models.DateField(blank=False,null=False,auto_now_add=True,verbose_name=u"日期")
    form_code = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"编号")
    returner = models.ForeignKey(User,blank=False,null=False,verbose_name=u'退料人',related_name="Steel_returner")
    inspector = models.ForeignKey(User,blank=True,null=True,verbose_name=u'检查员',related_name="steel_return_inspector")
    keeper = models.ForeignKey(User,blank=True,null=True,verbose_name=u"库管员",related_name="steel_return_keeper")
    return_confirm = models.BooleanField(default=False,verbose_name=u'退库单确认')
    steel_type = models.IntegerField(choices=STEEL_TYPE,default=0,verbose_name=u'钢材类型')#1:bar 0:board

    def __unicode__(self):
        return str(self.form_code)

    class Meta:
        verbose_name=u'钢材退库单'
        verbose_name_plural=u'钢材退库单'

class BoardSteelMaterialReturnCardContent(models.Model):
    steel_material = models.ForeignKey(SteelMaterial,blank=False,null=False,verbose_name=u"材料信息")
    card_info = models.ForeignKey(CommonSteelMaterialReturnCardInfo,blank=False,null=False,verbose_name=u"退库单表头")
    status = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"状态")
    quantity = models.IntegerField(blank=False,null=False,verbose_name=u"数量")
    weight = models.FloatField(blank=False,null=False,verbose_name=u"重量")
    #weight_management =models.IntegerField(choices=WEIGHT_MANAGEMENT,blank=False,null=False,verbose_name=u"重量单位")
    graph = models.CharField(max_length=100,blank=False,null=False,verbose_name=u"套料图")
    remark = models.CharField(max_length=100,blank=True,null=True,verbose_name=u"备注")

    def __unicode__(self):
        return str(self.card_info)

    class Meta:
        verbose_name=u"板材退库单详细信息"
        verbose_name_plural=u"板材退库单详细信息"

class BarSteelMaterialReturnCardContent(models.Model):
    steel_material = models.ForeignKey(SteelMaterial,blank=False,null=False,verbose_name=u'材料信息')
    card_info = models.ForeignKey(CommonSteelMaterialReturnCardInfo,blank=False,null=False,verbose_name=u"退库单表头")
    status = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"状态")
    quantity = models.IntegerField(blank=False,null=False,verbose_name=u"数量")
    weight = models.FloatField(blank=False,null=False,verbose_name=u"重量")
    length = models.FloatField(blank=False,null=False,verbose_name=u"长度")
    #length_management =models.IntegerField(choices=LENGHT_MANAGEMENT,blank=False,null=False,verbose_name=u"长度单位")
    remark = models.CharField(max_length=100,blank=True,null=True,verbose_name=u"备注")

    def __unicode__(self):
        return str(self.card_info)

    class Meta:
        verbose_name=u"型材退库单详细信息"
        verbose_name_plural=u"型材退库单详细信息"
"""

class WeldRefund(models.Model):
    department  = models.CharField(verbose_name=u"领用单位",max_length=20,blank=False)
    refund_code = models.CharField(verbose_name=u"编号",max_length=20,blank=False)
    create_time = models.DateField(blank=False,null=True,verbose_name=u"日期",auto_now_add = True)
    apply_card = models.OneToOneField(WeldingMaterialApplyCard,blank=False,verbose_name=u"领用单编号")
    refund_weight = models.FloatField(null=True,blank=False,verbose_name=u"退库量（重量）")
    refund_count = models.FloatField(null=True,blank=True,verbose_name=u"退库量（数量）")
    refund_status = models.CharField(max_length=20,blank=True,verbose_name=u"退库状态",default="")
    weldrefund_status = models.IntegerField(default=STORAGESTATUS_REFUNDER,choices=REFUNDSTATUS_CHOICES,verbose_name=u"退库单状态")
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
                                 default=STORAGESTATUS_PURCHASER,
                                 verbose_name=u'入库单状态')

    class Meta:
        verbose_name = u'辅助材料入库单'
        verbose_name_plural = u'辅助材料入库单'

    def __unicode__(self):
        return '%s' % self.entry_code

class AuxiliaryToolEntryItems(models.Model):
    name = models.CharField(blank=False, max_length=20,verbose_name=u"名称")
    specification = models.CharField(blank=True,max_length=20,verbose_name=u"规格")
    count = models.FloatField(verbose_name=u'入库数量',blank=False)
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
    inventory_count = models.FloatField(verbose_name=u"数量",blank=True,null=True)
    item_status = models.IntegerField(choices=WELD_ITEM_STATUS_CHOICES,default=0,verbose_name=u"材料状态",blank=False)
    entry_time=models.DateField(verbose_name=u'入库时间',blank=True,null=True)
    class Meta:
        verbose_name=u'辅助库存材料'
        verbose_name_plural=u'辅助库存材料'

    def __unicode__(self):
        return "%s(%s)" % (self.entry_item.name,self.entry_time)

    def save(self,*args,**kwargs):
        if self.inventory_count > 0 and self.item_status == ITEM_STATUS_SPENT:
            self.item_status = ITEM_STATUS_NORMAL #退库更新状态
        if self.item_status == ITEM_STATUS_NORMAL and self. inventory_count == 0:
            self.item_status = ITEM_STATUS_SPENT #领用更新状态
        super(AuxiliaryToolStoreList,self).save(*args,**kwargs)

class AuxiliaryToolApplyCard(models.Model):
    create_time=models.DateField(verbose_name=u'申请时间',auto_now_add=True)
    department = models.CharField(verbose_name=u"领用单位",max_length=50,blank=True,null=True)
    applycard_code = models.CharField(verbose_name=u"料单编号",max_length=20,blank=True,null=True)
    apply_storelist=models.ForeignKey(AuxiliaryToolStoreList,verbose_name=u'申请材料',blank=False,null=True,related_name="auap_apply_storelist")
    apply_quantity=models.IntegerField(verbose_name=u'申请数量',blank=False)
    actual_storelist = models.ForeignKey(AuxiliaryToolStoreList,verbose_name=u'实发材料',null=True,blank=True,related_name="auap_actual_storelist")
    actual_quantity=models.IntegerField(verbose_name=u'实发数量',default=0,blank=False)
    status=models.IntegerField(verbose_name=u'领用单状态',choices=AUXILIARY_TOOL_APPLY_CARD_STATUS,default=AUXILIARY_TOOL_APPLY_CARD_CREATED)
    applicant=models.ForeignKey(User,verbose_name=u'领料',blank=True,null=True,related_name="at_applicants")
    auditor = models.ForeignKey(User,verbose_name=u"主管",null=True,blank=True,related_name="at_auditor")
    keeper=models.ForeignKey(User,verbose_name=u'发料',blank=True,null=True,related_name="at_keeper")
    remark=models.TextField(verbose_name=u'备注',default="",blank=True,null=True)

    class Meta:
        verbose_name=u'辅助材料领用卡'
        verbose_name_plural=u'辅助材料领用卡'
    def __unicode__(self):
        return "%s" % self.apply_storelist.entry_item.name

class WeldStoreThread(models.Model):
    specification = models.CharField(max_length=50,verbose_name=u"规格")
    count = models.FloatField(verbose_name=u"数量")
    type=  models.CharField(verbose_name=u"材料种类",choices = MATERIAL_CATEGORY_CHOICES,max_length=20)
    class Meta:
        verbose_name = u"库存安全量"
        verbose_name_plural = u"库存安全量"
    def __unicode__(self):
        return '%s' % self.specification

class OutsideStandardEntry(StorageEntryBaseA):
    purchaser =  models.ForeignKey(User,blank=True,null=True,verbose_name=u"采购员",related_name = "out_purchaser")
    inspector = models.ForeignKey(User,blank=True,null=True,verbose_name=u"检验员",related_name = "out_inspector")
    keeper = models.ForeignKey(User,blank=True,null=True,verbose_name=u"库管员" , related_name = "out_keeper")
    entry_status = models.IntegerField(choices=ENTRYSTATUS_CHOICES,default=STORAGESTATUS_INSPECTOR,verbose_name=u"入库单状态")
    bidform  =  models.ForeignKey(BidForm,verbose_name=u"订购单编号",max_length=20,blank=True,null=True)
    class Meta:
        verbose_name = u"外购件入库单"
        verbose_name_plural = u"外购件入库单"

class OutsideStandardItem(StorageEntryItemBaseA):
    entry = models.ForeignKey(OutsideStandardEntry,verbose_name = u"入库单")
    class Meta:
        verbose_name = u"外购件材料"
        verbose_name_plural = u"外购件材料"
    def __unicode__(self):
        return '%s(%s)' % (self.specification, self.entry)

class OutsideApplyCard(ApplyCardBase):
    proposer = models.ForeignKey(User,blank=True,null=True,verbose_name=u"领用人",related_name = "out_apply_proposer")
    auditor = models.ForeignKey(User,blank=True,null=True,verbose_name=u"审核人",related_name = "out_apply_auditor")
    inspector = models.ForeignKey(User,blank=True,null=True,verbose_name=u"检验员",related_name = "out_apply_inspector")
    keeper = models.ForeignKey(User,blank=True,null=True,verbose_name=u"库管员" , related_name = "out_apply_keeper")
    entry_status = models.IntegerField(choices=APPLYCARDSTATUS_CHOICES,default=STORAGESTATUS_AUDITOR,verbose_name=u"入库单状态")

    class Meta:
        verbose_name = u"外购件领用单"
        verbose_name_plural = u"外购件领用单"
    def __unicode__(self):
        return self.entry_code

class OutsideStorageList(models.Model):
    texture = models.CharField(verbose_name=u"材质",max_length=50,blank=True,null=True)
    specification = models.CharField(verbose_name=u"规格",max_length=20,blank=True,null=True)
    number = models.IntegerField(verbose_name=u"数量")
    unit = models.CharField(verbose_name=u"单位",max_length=20,blank=True,null=True)
    class Meta:
        verbose_name = u"外购件库存"
        verbose_name_plural = u"外购件库存"
    def __unicode__(self):
        return '%s' % self.specification
class OutsideApplyCardItem(ApplyCardItemBase):
    applycard = models.ForeignKey(OutsideApplyCard,verbose_name=u"领用单")
    class Meta:
        verbose_name = u"外购件领用单材料"
        verbose_name_plural = u"外购件领用单材料"
    def __unicode__(self):
        return "%s(%s)" % (self.specification,self.applycard)
