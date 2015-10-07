# coding: UTF-8
from django.db import models
from const.models import BidFormStatus,Materiel,WorkOrder
from django.contrib.auth.models import User
import settings

# Create your models here.
class OrderForm(models.Model):
    order_id = models.CharField(unique = True, max_length = 20, blank = False, verbose_name = u"订购单编号")
    create_time = models.DateTimeField(null = True, verbose_name = u"创建日期")
    establishment_time = models.DateTimeField(null = True, verbose_name = u"编制日期")
    order_status = models.ForeignKey(OrderFormStatus, null = False, verbose_name = u"订购单状态")
    class Meta:
        verbose_name = u"订购单"
        verbose_name_plural = u"订购单"
    def __unicode__(self):
        return self.order_id

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

class bidApply(models.Model):
    apply_id = models.CharField(unique=True, max_length=20, blank=False, verbose_name=u"标单申请编号")
    apply_company = models.CharField(null=True, max_length=40, verbose_name=u"申请单位")
    demand_company = models.CharField(null=True, max_length=40, verbose_name=u"需求单位")
    work_order = models.ForeignKey(BidFormStatus,null=False,verbose_name=u"工作令")
    amount = models.IntegerField(verbose_name=u"数量")
    bid_project = models.CharField(null=True, max_length=40, verbose_name=u"拟招(议)项目")
    bid_date = models.DateTimeField(null=True, verbose_name=u"拟招(议)标时间")
    special_model = models.CharField(null=True, max_length=40, verbose_name=u"规格、型号")
    core_part = models.BooleanField(verbose_name="是否为核心件")

    class Meta:
        verbose_name = u"标单申请表"

    def __unicode__(self):
        return '%s'% (self.apply_id)

class qualityPriceCard(models.Model):
    apply_id = models.CharField(unique=True, max_length=20, blank=False, verbose_name=u"标单申请编号")
    apply_company = models.CharField(null=True, max_length=40, verbose_name=u"申请单位")
    demand_company = models.CharField(null=True, max_length=40, verbose_name=u"需求单位")
    work_order = models.ForeignKey(BidFormStatus,null=False,verbose_name=u"工作令")
    amount = models.IntegerField(verbose_name=u"数量")
    unit = models.CharField(null=True, max_length=40, verbose_name=u"单位")
    content = models.CharField(null=True, max_length=40, verbose_name=u"内容")
    material = models.CharField(null=True, max_length=40, verbose_name=u"材质")
    delivery_period = models.CharField(null=True, max_length=40, verbose_name=u"交货期")
    price = models.CharField(null=True, max_length=40, verbose_name=u"价格")
    ability = models.CharField(null=True, max_length=40, verbose_name=u"厂家协作能力质量情况及业绩")
    delivery_condition = models.CharField(null=True, max_length=40, verbose_name=u"交货及支付条件")
    class Meta:
        verbose_name = u"标单申请表"

    def __unicode__(self):
        return '%s'% (self.apply_id)

class Supplier(models.Model):
    supplier_id=models.CharField(unique=True,max_length=20,blank=False,verbose_name=u"供应商编号")
    supplier_name=models.CharField(max_length=50,blank=False,verbose_name=u"供应商名称")
    class Meta:
        verbose_name = u"供应商"
        verbose_name_plural = u"供应商"
    def __unicode__(self):
        return '%s'% (self.supplier_name)

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

class ArrivalInspection(models.Model):
    material_confirm = models.BooleanField(null=False,default=False,verbose_name=u"实物确认")
    soft_confirm = models.BooleanField(null=False,default=False,verbose_name=u"软件确认")
    inspect_confirm = models.BooleanField(null=False,default=False,verbose_name=u"检验通过")
    bidform = models.ForeignKey(BidForm,null=False,verbose_name=u"标单号")
    material = models.ForeignKey(Materiel,verbose_name=u"材料") 
    class Meta:
        verbose_name = u"到货检验"
        verbose_name_plural = u"到货检验"

    def __unicode__(self):
        return '%s(%s)' % (self.bidform.bid_id,self.material.name)

class PurchasingEntry(models.Model):
    entry_time = models.DateField(blank=True, null=True,verbose_name=u"入库时间")
    receipts_code = models.CharField(max_length=100,blank=False,verbose_name=u"单据编号")
    purchaser =  models.ForeignKey(User,blank=False,verbose_name=u"采购员",related_name = "purchaser")
    inspector = models.ForeignKey(User,blank=False,verbose_name=u"检验员",related_name = "inspector")
    keeper = models.ForeignKey(User,blank=False,verbose_name=u"库管员" , related_name = "keeper")
    entry_confirm = models.BooleanField(null=False,default=False,verbose_name=u"入库单确认")
    bidform = models.ForeignKey(BidForm,verbose_name=u"标单号")
    
    class Meta:
        verbose_name = u"入库单"
        verbose_name_plural = u"入库单"

    def __unicode__(self):
        return '%s' % self.bidform.bid_id

class PurchasingEntryItems(models.Model):
    material = models.ForeignKey(Materiel,blank = True , null = True , verbose_name = u"材料")
    standard = models.CharField(max_length = 100 , blank = True,null = True,verbose_name = u"标准")
    status = models.CharField(max_length = 100,blank = True, null = True , verbose_name = u"状态")
    remark = models.CharField(max_length = 100, blank = True , null = True , verbose_name = u"备注")
    purchasingentry = models.ForeignKey(PurchasingEntry,verbose_name = u"入库单")
    class Meta:
        verbose_name = u"入库材料"
        verbose_name_plural = u"入库材料"
    def __unicode__(self):
        return '%s(%s)' % (self.material.name, self.purchasingentry)

class MaterielPurchasingStatus(models.Model):
    materiel = models.OneToOneField(Materiel)
    add_to_detail = models.BooleanField(default = False)
    class Meta:
        verbose_name = u"物料采购状态"
        verbose_name_plural = u"物料采购状态"
    def __unicode__(self):
       return self.materiel.name

class MaterialSubApply(models.Model):
    receipts_code = models.CharField(max_length = 100, blank = False , verbose_name = u"单据编号")
    pic_code =  models.CharField(max_length = 100, blank = False , verbose_name = u"图号")
    work_order = models.ForeignKey(WorkOrder,verbose_name = u"工作令")
    bidform = models.ForeignKey(BidForm,blank = True , null = True, verbose_name = u"对应标单")
    reasons = models.CharField(max_length = 1000,blank = True , null = True, verbose_name = u"代用原因和理由")
    class Meta:
        verbose_name = u"材料代用申请单"
        verbose_name_plural = u"材料代用申请单"
    def __unicode__(self):
        return self.receipts_code

class MaterialSubApplyItems(models.Model):
    mat_pic_code = models.CharField(max_length = 100, blank = False , verbose_name = u"部件图号")
    pic_ticket_code = models.CharField(max_length = 100, blank = False , verbose_name = u"零件图号或票号")
    old_name = models.CharField(max_length = 100, blank = False , verbose_name = u"原材料名称")
    old_standard = models.CharField(max_length = 100, blank = False , verbose_name = u"原材料标准")
    old_size = models.CharField(max_length = 100, blank = False , verbose_name = u"原材料规格和尺寸")
    new_name = models.CharField(max_length = 100, blank = False , verbose_name = u"拟用材料名称")
    new_standard = models.CharField(max_length = 100, blank = False , verbose_name = u"拟用材料标准")
    new_size = models.CharField(max_length = 100, blank = False , verbose_name = u"拟用材料规格和尺寸")
    sub_apply = models.ForeignKey(MaterialSubApply,verbose_name = u"材料代用申请单")
    class Meta:
        verbose_name = u"材料代用申请条目"
        verbose_name_plural = u"材料代用申请条目"
    def __unicode__(self):
        return "%s(%s)" % (self.sub_apply,self.mat_pic_code) 
