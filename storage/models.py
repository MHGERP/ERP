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
from storage.utils import get_today
# Create your models here.


class StorageEntryBaseA(models.Model):
    change_code = models.CharField(verbose_name=u"修改号",max_length=20,blank=True,null=True)
    sample_report = models.CharField(verbose_name=u"样表",max_length=20,blank=True,null=True)
    entry_code = models.CharField(verbose_name=u"单据编号",max_length=20,unique=True)
    source  = models.CharField(verbose_name=u"货物来源",max_length=20,blank=True,null=True)
    inspection_record = models.CharField(verbose_name=u"检查记录表编号",max_length=20,blank=True,null=True)
    order_number =  models.CharField(verbose_name=u"订购单编号",max_length=20,blank=True,null=True)
    remark = models.CharField(verbose_name=u"备注",max_length=200,blank=True,null=True)
    entry_time = models.DateField(verbose_name=u"入库时间",null=True,auto_now=True)

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
    entry_time = models.DateField(blank=False, null=True,verbose_name=u"入库时间")
    purchaser =  models.ForeignKey(User,blank=True,null=True,verbose_name=u"采购员",related_name = "purchaser")
    inspector = models.ForeignKey(User,blank=True,null=True,verbose_name=u"检验员",related_name = "inspector")
    keeper = models.ForeignKey(User,blank=True,null=True,verbose_name=u"库管员" , related_name = "keeper")
    bidform = models.ForeignKey(BidForm,verbose_name=u"标单号")
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
    date = models.DateField( blank = False ,null = True, verbose_name = u"生产日期")
    price = models.FloatField( blank = True ,default="0", verbose_name = u"价格")
    entry = models.ForeignKey(WeldMaterialEntry,verbose_name = u"入库单")
    class Meta:
        verbose_name = u"焊材入库材料"
        verbose_name_plural = u"焊材入库材料"
    def __unicode__(self):
        return '%s(%s)' % (self.material.name, self.entry)

class WeldStoreListManager(models.Manager):
    def qualified_set(self):
        print get_today()
        return self.filter(deadline__gte = get_today()) 

class WeldStoreList(models.Model):
    factory = models.CharField(max_length=20,null = True,verbose_name=u"厂家")
    deadline = models.DateField(verbose_name=u"最后期限",null = True)
    brand = models.CharField(max_length=20,verbose_name=u"牌号",null=True)
    specification = models.CharField(max_length=50,verbose_name=u"规格")
    count = models.FloatField(verbose_name=u"数量")
    entry_time = models.DateField(verbose_name=u"入库时间")
    charge_number = models.CharField(max_length=20,verbose_name=u"材料批号",null=True)
    material_id = models.CharField(max_length=20,verbose_name=u"材质编号")
    remark = models.CharField(max_length=100,verbose_name=u"备注",null = True)
    entry_item = models.ForeignKey(WeldMaterialEntryItems,verbose_name = u"焊材入库单材料")

    objects = WeldStoreListManager()
    class Meta:
        verbose_name = u"焊材库存清单"
        verbose_name_plural = u"焊材库存清单"

    def __unicode__(self):
        return "%s(%s)" % (self.specification,self.factory)

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
    material_number=models.CharField(verbose_name=u'材质编号',max_length=20,blank=True,null=True)
    actual_weight=models.FloatField(verbose_name=u'实发重量',default=-1,blank=False)
    actual_quantity=models.FloatField(verbose_name=u'实发数量',default=-1,blank=False)
    applicant=models.ForeignKey(User,verbose_name=u'领用人',blank=False,related_name="applicants")
    auditor=models.ForeignKey(User,verbose_name=u'审核人',default=None,blank=True,null=True,related_name="auditors")
    inspector=models.ForeignKey(User,verbose_name=u'检查员',default=None,blank=True,null=True,related_name="inspectors")
    commit_user=models.ForeignKey(User,verbose_name=u'发料人',default=None,blank=True,null=True,related_name="commit_users")
    status=models.IntegerField(verbose_name=u'领用状态',choices=APPLYCARD_STATUS_CHOICES,default=APPLYCARD_APPLY,blank=False)
    storelist = models.ForeignKey(WeldStoreList,null = True,verbose_name=u'库存材料')
    def __unicode__(self):
        return str(self.index)


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
        verbose_name_plural=u'焊焊材库温湿度记录卡'    

class SteelMaterialPurchasingEntry(models.Model):
    material_source = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'货物来源')
    form_code = models.CharField(max_length=20,blank=False,null=False,verbose_name="入库单编号")
    purchaser =  models.ForeignKey(User,blank=False,null=False,related_name="steel_purchaser",verbose_name=u"采购员")
    inspector = models.ForeignKey(User,blank=False,null=False,related_name="steel_inspector",verbose_name=u"检验员",)
    keeper = models.ForeignKey(User,blank=False,null=False,related_name = "steel_keeper",verbose_name=u"库管员" ,)
    entry_time = models.DateField(blank=False,null=True,auto_now_add=True,verbose_name=u"入库时间")
    entry_confirm = models.BooleanField(default=False,verbose_name=u"入库单确认")
    steel_type = models.IntegerField(choices = ENTRYTYPE_CHOICES_2,default=0,verbose_name=u"入库单类型")
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
    material = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'材质')
    material_number = models.CharField(max_length=20,blank=False,null=False,verbose_name=u'材质编号')
    return_time = models.IntegerField(default=0,verbose_name=u'退库次数')
    #entry_form = models.ForeignKey(SteelMaterialPurchasingEntry,blank=False,null=False,verbose_name=u'表头')
    work_order = models.ManyToManyField(WorkOrder,blank=False,null=False,verbose_name=u'工作令')
    steel_type = models.IntegerField(choices=STEEL_TYPE,blank=False,null=False,default=0,verbose_name=u'钢材类型')
    store_room = models.ForeignKey(StoreRoom,blank=False,null=False,verbose_name=u'库房位置')
    #remark = models.CharField(max_length=50,blank=True,null=True,verbose_name="备注")

    def __unicode__(self):
        return "%s(%s)"%(self.name,self.specifications)

    def show_workorder(self):
        workorder_set = self.work_order.all()
        work_order_list = []
        for order in workorder_set:
            work_order_list.append(order.order_index)
        work_order_str = ','.join(work_order_list)
        return work_order_str

    class Meta:
        verbose_name=u'钢材参数信息'
        verbose_name_plural=u'钢材参数信息'



class BoardSteelMaterialPurchasingEntry(models.Model):
    steel_material = models.ForeignKey(SteelMaterial,blank=False,null=False,verbose_name=u"材料信息")
    card_info = models.ForeignKey(SteelMaterialPurchasingEntry,blank=False,null=False,verbose_name=u"入库单表头")
    status = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"状态")
    quantity = models.IntegerField(blank=False,null=False,verbose_name=u"数量")
    weight = models.FloatField(blank=False,null=False,verbose_name=u"重量")
    weight_management =models.IntegerField(choices=WEIGHT_MANAGEMENT,blank=False,null=False,verbose_name=u"重量单位")
    remark = models.CharField(max_length=100,blank=True,null=True,verbose_name=u"备注")

    def __unicode__(self):
        return str(self.card_info)

    class Meta:
        verbose_name=u"板材入库单详细信息"
        verbose_name_plural=u"板材入库单详细信息"

class BarSteelMaterialPurchasingEntry(models.Model):
    steel_material = models.ForeignKey(SteelMaterial,blank=False,null=False,verbose_name=u'材料信息')
    card_info = models.ForeignKey(SteelMaterialPurchasingEntry,blank=False,null=False,verbose_name=u"入库单表头")
    status = models.CharField(max_length=20,blank=False,null=False,verbose_name=u"状态")
    quantity = models.IntegerField(blank=False,null=False,verbose_name=u"数量")
    length = models.FloatField(blank=False,null=False,verbose_name=u"长度")
    length_management =models.IntegerField(choices=LENGHT_MANAGEMENT,blank=False,null=False,verbose_name=u"长度单位")
    remark = models.CharField(max_length=100,blank=True,null=True,verbose_name=u"备注")

    def __unicode__(self):
        return str(self.card_info)

    class Meta:
        verbose_name=u"型材入库单详细信息"
        verbose_name_plural=u"型材入库单详细信息"


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
    weight_management = models.IntegerField(choices=WEIGHT_MANAGEMENT,default=0,blank=False,null=False,verbose_name=u'重量单位')
    area = models.FloatField(blank=False,null=False,verbose_name=u'钢板面积',default=0)
    area_management = models.IntegerField(choices=AREA_MANAGEMENT,default=0,blank=False,null=False,verbose_name=u'面积单位')
    # store_room = models.ForeignKey(StoreRoom,blank=False,null=False,verbose_name=u'库房位置')
    slice_cad = models.CharField(max_length=50,blank=True,null=True,verbose_name=u'套料图')

    def __unicode__(self):
        return "%s(%s)"%(self.material_info.name,self.material_info.specifications)

    class Meta:
        verbose_name=u'板材台账'
        verbose_name_plural=u'板材台账'

class BarSteelMaterialLedger(models.Model):
    material_info = models.OneToOneField(SteelMaterial,blank=False,null=False,verbose_name=u"钢材信息")
    quantity = models.IntegerField(blank=False,null=False,verbose_name=u'型材数量')
    # store_room = models.ForeignKey(StoreRoom,blank=False,null=False,verbose_name=u'库房位置')
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
    steel_type = models.IntegerField(choices=STEEL_TYPE,default=0,verbose_name=u'钢材类型')

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
    weight_management =models.IntegerField(choices=WEIGHT_MANAGEMENT,blank=False,null=False,verbose_name=u"重量单位")
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
    length = models.FloatField(blank=False,null=False,verbose_name=u"长度")
    length_management =models.IntegerField(choices=LENGHT_MANAGEMENT,blank=False,null=False,verbose_name=u"长度单位")
    remark = models.CharField(max_length=100,blank=True,null=True,verbose_name=u"备注")

    def __unicode__(self):
        return str(self.card_info)

    class Meta:
        verbose_name=u"型材退库单详细信息"
        verbose_name_plural=u"型材退库单详细信息"

class WeldRefund(models.Model):
    department = models.ForeignKey(Group,max_length=20,blank=False,verbose_name=u"退库单位")
    date = models.DateField(blank=False,null=True,verbose_name=u"日期",auto_now_add = True)
    code = models.CharField(max_length=20,blank=False,null=True,unique=True,verbose_name=u"编号")
    work_order = models.ForeignKey(WorkOrder,verbose_name=u"工作令")
    receipts_time = models.DateField(blank=False,null=True,verbose_name=u"领用日期")
    receipts_code = models.OneToOneField(WeldingMaterialApplyCard,blank=False,verbose_name=u"领用编号")
    specification = models.CharField(max_length=50,blank=False,null=True,verbose_name=u"型号规格") 
    refund_weight = models.FloatField(default=0,blank=False,verbose_name=u"退库量（重量）")
    refund_count = models.FloatField(default=0,blank=False,verbose_name=u"退库量（数量）")
    refund_status = models.CharField(max_length=20,blank=False,null=True,verbose_name=u"退库状态")
    weldrefund_status = models.IntegerField(default=STORAGESTATUS_KEEPER,choices=REFUNDSTATUS_CHOICES,verbose_name=u"退库单状态")
    refunder =  models.ForeignKey(User,verbose_name=u"退库人",related_name = "weldrefund_refunder")
    keeper = models.ForeignKey(User,verbose_name=u"库管人",related_name = "weldrefund_keeper")   

    class Meta:
        verbose_name = u"焊接材料退库卡"
        verbose_name_plural = u"焊接材料退库卡"

    def __unicode__(self):
        return '%s' % self.code


class AuxiliaryTool(models.Model):
    name=models.CharField(verbose_name=u'材料名称',max_length=30,blank=False)
    model=models.IntegerField(verbose_name=u'类别',blank=False,choices=AUXILIARY_TOOLS_MODELS_CHOICES)
    measurement_unit=models.CharField(verbose_name=u'计量单位',max_length=10,blank=False)
    quantity=models.FloatField(verbose_name=u'数量',default=0,blank=False)
    unit_price=models.FloatField(verbose_name=u'单价',blank=False)
    manufacturer=models.CharField(verbose_name=u'厂家',max_length=30,blank=False)

    class Meta:
        verbose_name=u'辅助材料'
        verbose_name_plural=u'辅助材料'

    def __unicode__(self):
        return self.name+u' 制造:'+self.manufacturer

class AuxiliaryToolApplyCard(models.Model):
    create_time=models.DateField(verbose_name=u'申请时间',auto_now_add=True)
    commit_time=models.DateField(verbose_name=u'实发时间',blank=True,null=True)
    index=models.IntegerField(verbose_name=u'编号',default=0,blank=False,unique=True)
    apply_item=models.ForeignKey(AuxiliaryTool,verbose_name=u'申请物资',blank=False,related_name="apply_items")
    apply_quantity=models.IntegerField(verbose_name=u'申请数量',blank=False)
    apply_total=models.FloatField(verbose_name=u'申请总价',default=0,blank=False)#overwrite the save() method to calculate the apply_total

    actual_item=models.ForeignKey(AuxiliaryTool,verbose_name=u'实发物资',default=None,blank=True,null=True,related_name="actual_items")
    actual_quantity=models.IntegerField(verbose_name=u'实发数量',default=0,blank=False)
    actual_total=models.FloatField(verbose_name=u'实际总价',default=0,blank=False)
    status=models.IntegerField(verbose_name=u'完成状态',choices=AUXILIARY_TOOL_APPLY_CARD_STATUS,default=AUXILIARY_TOOL_APPLY_CARD_CREATED,blank=False)
    applicant=models.ForeignKey(User,verbose_name=u'领用人',default=None,blank=True,null=True,related_name="at_applicants")
    commit_user=models.ForeignKey(User,verbose_name=u'确认人',default=None,blank=True,null=True,related_name="at_commit_users")
    remark=models.TextField(verbose_name=u'备注',default=None,blank=True,null=True)
    def save(self,*args,**kwargs):
        if not self.index:
            self.index=randint(0,10000000)
        if self.status==AUXILIARY_TOOL_APPLY_CARD_APPLYED:
            self.apply_total=self.apply_item.unit_price*self.apply_quantity
        elif self.status==AUXILIARY_TOOL_APPLY_CARD_COMMITED:
            self.commit_time=timezone.now()
        super(AuxiliaryToolApplyCard,self).save(*args,**kwargs)

    class Meta:
        verbose_name=u'辅助材料领用卡'
        verbose_name_plural=u'辅助材料领用卡'
    def __unicode__(self):
        return str(self.index)



class AuxiliaryToolEntryCardList(models.Model):
    create_time = models.DateField(verbose_name=u'创建时间', auto_now_add=True)
    workorder = models.ForeignKey(WorkOrder, verbose_name=u'工作令',
                                  blank=True, null=True)
    purchaser = models.ForeignKey(User, blank=True, null=True,
                                  verbose_name=u'采购员', related_name='au_purchaser')
    inspector = models.ForeignKey(User, blank=True, null=True,
                                  verbose_name=u'检验员', related_name='au_inspector')
    keeper = models.ForeignKey(User, blank=True, null=True,
                               verbose_name=u'库管员', related_name='au_keeper')
    index = models.CharField(blank=False, null=False, max_length=20,
                             verbose_name=u'编号', unique=True)
    status = models.IntegerField(choices=ENTRYSTATUS_CHOICES,
                                 default=STORAGESTATUS_PURCHASER,
                                 verbose_name=u'入库单状态')

    class Meta:
        verbose_name = u'辅助材料入库单'
        verbose_name_plural = u'辅助材料入库单'

    def __unicode__(self):
        return '%s' % self.index

class AuxiliaryToolEntryCard(models.Model):
    create_time=models.DateField(verbose_name=u'创建时间',auto_now_add=True)
    auxiliary_tool=models.ForeignKey(AuxiliaryTool,verbose_name=u'入库材料',blank=False)
    quantity=models.FloatField(verbose_name=u'入库数量',blank=False)
    card_list=models.ForeignKey(AuxiliaryToolEntryCardList, blank=True,
                                null=True, verbose_name=u'入库单')

    class Meta:
        verbose_name=u'辅助材料入库单项'
        verbose_name_plural=u'辅助材料入库单项'

    def __unicode__(self):
        return u'%s %s %s'%(self.auxiliary_tool,self.quantity,self.create_time)


class WeldStoreThread(models.Model):
    specification = models.CharField(max_length=50,verbose_name=u"规格")
    count = models.FloatField(verbose_name=u"数量")
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
