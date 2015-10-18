# coding: UTF-8
from const import *
import datetime
from const import MATERIEL_CHOICE
from django.db import models
from const.models import BidFormStatus,Materiel, WorkOrder, OrderFormStatus, ImplementClassChoices
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
    create_time=models.DateTimeField(blank=True,null=True,verbose_name=u"创建日期")
    establishment_time=models.DateTimeField(blank=True,null=True,verbose_name=u"编制日期")
    audit_time=models.DateTimeField(blank=True,null=True,verbose_name=u"审核日期")
    approved_time=models.DateTimeField(blank=True,null=True,verbose_name=u"批准日期")
    bid_status=models.ForeignKey(BidFormStatus,null=False,verbose_name=u"标单状态")

    class Meta:
        verbose_name = u"标单"
        verbose_name_plural = u"标单"
    def __unicode__(self):
        return '%s'% (self.bid_id)

class BidComment(models.Model):
    user = models.ForeignKey(User, blank = False)
    comment = models.CharField(max_length=400,blank=False,verbose_name=u"审批意见")
    bid = models.ForeignKey(BidForm, blank = False)
    submit_date=models.DateField(blank=True,null=True,default=lambda: datetime.datetime.today(),verbose_name=u"提交日期")
    result=models.IntegerField(choices=APPROVED_RESULT_CHOICES,verbose_name=u"审批结果")
    status=models.IntegerField(choices=BIDFORM_STATUS_CHOICES,verbose_name=u"状态")
    class Meta:
        verbose_name = u"标单评审意见"
        verbose_name_plural = u"标单评审意见"
    def __unicode__(self):
        return '%s'% (self.id)

class MaterielFormConnection(models.Model):
    materiel = models.OneToOneField(Materiel, blank = False, verbose_name = u"物料")
    order_form = models.ForeignKey(OrderForm, blank = True, null = True, verbose_name = u"订购单")
    bid_form = models.ForeignKey(BidForm, blank = True, null = True, verbose_name = u"标单")
    count = models.CharField(blank = True, null = True, max_length = 20, verbose_name = u"需求数量")
    class Meta:
        verbose_name = u"物料——采购——关联表"
        verbose_name_plural = u"物料——采购——关联表"
    def __unicode__(self):
        return self.materiel.name

import uuid
def make_uuid():
    """
    make uuid
    """
    return str(uuid.uuid4())

class bidApply(models.Model):
    apply_id = models.CharField(unique=True, max_length=50, default=make_uuid, verbose_name=u"标单申请编号")
    apply_company = models.CharField(null=True, max_length=40, verbose_name=u"申请单位")
    demand_company = models.CharField(null=True, max_length=40, verbose_name=u"需求单位")
    amount = models.IntegerField(verbose_name=u"数量", default = 0)
    work_order = models.ForeignKey(WorkOrder,null=False,verbose_name=u"工作令")
    bid_project = models.CharField(null=True, max_length=40, verbose_name=u"拟招(议)项目")
    bid_date = models.DateTimeField(null=True, verbose_name=u"拟招(议)标时间")
    special_model = models.CharField(null=True, max_length=40, verbose_name=u"规格、型号")
    core_part = models.BooleanField(verbose_name="是否为核心件", default = False)

    bid = models.ForeignKey(BidForm)
    project_category = models.CharField(null=True, blank=True, max_length=40, verbose_name=u"项目类别")
    bid_datetime = models.DateTimeField(null=True, blank=True, default=lambda: datetime.datetime.today(), verbose_name=u"招(议)标时间")
    bid_delivery_date = models.DateTimeField(null=True, blank=True, default=lambda: datetime.datetime.today(), verbose_name=u"标书递送时间")
    place = models.CharField(null=True, blank=True, max_length=40, verbose_name=u"地点")
    try:
        default_status = ImplementClassChoices.objects.get(category = 0).id
    except:
        default_status = 1
    implement_class = models.ForeignKey(ImplementClassChoices, blank=False, default=default_status, verbose_name=u"实施类别")

    class Meta:
        verbose_name = u"标单申请表"

    def __unicode__(self):
        return '%s'% (self.apply_id)

class qualityPriceCard(models.Model):
    bid = models.ForeignKey(BidForm, blank = False)
    apply_id = models.CharField(unique=True, max_length=20, blank=False, verbose_name=u"标单申请编号")
    apply_company = models.CharField(null=True, max_length=40, verbose_name=u"申请单位")
    demand_company = models.CharField(null=True, max_length=40, verbose_name=u"需求单位")
    work_order = models.ForeignKey(WorkOrder,null=False,verbose_name=u"工作令")
    amount = models.IntegerField(verbose_name=u"数量")
    unit = models.CharField(null=True, max_length=40, verbose_name=u"单位")
    content = models.CharField(null=True, max_length=40, verbose_name=u"内容")
    material = models.CharField(null=True, max_length=40, verbose_name=u"材质")
    delivery_period = models.CharField(null=True, max_length=40, verbose_name=u"交货期")
    price = models.CharField(null=True, max_length=40, verbose_name=u"价格")
    ability = models.CharField(null=True, max_length=40, verbose_name=u"厂家协作能力质量情况及业绩")
    delivery_condition = models.CharField(null=True, max_length=40, verbose_name=u"交货及支付条件")
    class Meta:
        verbose_name = u"比质比价卡"

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
    standard = models.CharField(max_length = 100 , blank = True,default="", verbose_name = u"标准")
    status = models.CharField(max_length = 100,blank = True,default="", verbose_name = u"状态")
    remark = models.CharField(max_length = 100, blank = True , default="" , verbose_name = u"备注")
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

class SupplierSelect(models.Model):
    bidform=models.ForeignKey(BidForm,blank=False,verbose_name=u"标单")
    supplier=models.ForeignKey(Supplier,blank=False,verbose_name=u"供应商")
    class Meta:
        verbose_name = u"供应商选择"
        verbose_name_plural = u"供应商选择"
        unique_together = (("bidform", "supplier", ), )
    def __unicode__(self):
        return "%s select %s" % (self.bidform.bid_id, self.supplier.supplier_name)
class MaterialSubApply(models.Model):
    receipts_code = models.CharField(max_length = 100, unique = True, blank = False ,null = True, verbose_name = u"单据编号")
    pic_code =  models.CharField(max_length = 100, blank = False , null = True, verbose_name = u"图号")
    work_order = models.ForeignKey(WorkOrder,verbose_name = u"工作令" , blank = True , null = True)
    bidform = models.ForeignKey(BidForm,blank = True , null = True, verbose_name = u"对应标单")
    reasons = models.CharField(max_length = 1000,blank = True , null = True, verbose_name = u"代用原因和理由")
    proposer = models.ForeignKey(User,verbose_name = u"申请人",blank = True)
    is_submit = models.BooleanField(default = False,verbose_name = u"是否提交")
    comments = models.CharField(max_length=1000,blank = True , null = True, verbose_name = u"评审意见")
    is_approval = models.IntegerField(choices = REVIEW_COMMENTS_CHOICES,default = -1 ,verbose_name = u"评审结果",blank = True)
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

class MaterielExecute(models.Model):
    document_number = models.CharField(max_length = 100, blank = False, verbose_name = u"单据编号")
    document_lister = models.ForeignKey(User, blank = False, verbose_name = u"制表人")
    date_date = models.DateField(blank = False, null = False, verbose_name = u"制表日期")
    materiel_choice = models.CharField(blank=False, max_length = 20, choices=MATERIEL_CHOICE, verbose_name=u"材料选择")
    class Meta:
        verbose_name = u"材料执行表"
        verbose_name_plural = u"材料执行表"
    def __unicode__(self):
        return '%s' % self.document_number

class MainMaterielExecuteDetail(models.Model):
    materiel_execute = models.OneToOneField(MaterielExecute)
    materiel_name = models.CharField(max_length=50, blank=False, verbose_name = u"名称")
    materiel_texture = models.ForeignKey(Materiel, verbose_name = u"材质")
    quality_class = models.CharField(max_length=20, blank=False, verbose_name = u"质量分类")
    specification = models.CharField(max_length=100, blank=False, verbose_name= u"规格")
    quantity = models.IntegerField(verbose_name = u"数量")
    purchase_weight = models.FloatField(verbose_name = u"采购")
    recheck = models.BooleanField(default = False, verbose_name = u"复验")
    crack_rank = models.CharField(max_length = 20, blank = False, verbose_name = u"探伤级别")
    delivery_status = models.CharField(max_length = 50, blank = False, verbose_name = u"交货状态")
    execute_standard = models.CharField(max_length = 100, blank = False, verbose_name = u"执行标准")
    remark = models.CharField(max_length = 200, blank = True, verbose_name = u"备注")
    class Meta:
        verbose_name = u"主材材料执行表详细"
        verbose_name_plural = u"主材材料执行表详细"
    def __unicode__(self):
        return "%s(%s)" % (self.materiel_execute.document_number, self.materiel_texture.index)

class ProcessFollowingInfo(models.Model):
    bidform=models.ForeignKey(BidForm,blank=False,verbose_name=u"标单")
    following_date=models.DateField(blank=False,null=False,verbose_name=u"跟踪日期")
    following_method=models.CharField(blank=False,null=False,max_length=20,verbose_name=u"跟踪方式")
    following_feedback=models.CharField(blank=False,null=False,max_length=500,verbose_name=u"跟踪反馈")
    file_obj = models.FileField(blank=True,upload_to=settings.PROCESS_FILE_PATH +"/%Y/%m/%d",verbose_name="文件对象")
    executor=models.ForeignKey(User,verbose_name=u"执行人")
    inform_tech=models.BooleanField(default=False,verbose_name=u"是否通知工艺")
    class Meta:
        verbose_name = u"过程跟踪记录"
        verbose_name_plural = u"过程跟踪记录"
    def __unicode__(self):
        return self.bidform.bid_id
class SupportMaterielExecuteDetail(models.Model):
    materiel_execute = models.OneToOneField(MaterielExecute)
    materiel_texture = models.ForeignKey(Materiel, blank = False, verbose_name = u"材质")
    texture_number = models.CharField(max_length = 100, blank = False, verbose_name = u"材质编号")
    specification = models.CharField(max_length = 100, blank = False, verbose_name = u"规格")
    quantity = models.IntegerField(verbose_name = u"数量")
    delivery_status = models.CharField(max_length = 50, blank = False, verbose_name = u"交货状态")
    press = models.CharField(max_length = 50, blank = False, verbose_name = u"受压")
    crack_rank = models.CharField(max_length = 20, blank = False, verbose_name = u"探伤级别")
    recheck = models.BooleanField(default = False, verbose_name = u"复验")
    quota = models.CharField(max_length = 50, blank = True, verbose_name = u"定额")
    part = models.CharField(max_length = 50, blank = True, verbose_name = u"零件")
    oddments = models.CharField(max_length = 50, blank = True, verbose_name = u"余料")
    remark = models.CharField(max_length = 200, blank = True, verbose_name = u"备注")
    class Meta:
        verbose_name = u"辅材材料执行表详细"
        verbose_name_plural = u"辅材材料执行表详细"
    def __unicode__(self):
        return "%s(%s)" % (self.materiel_execute.document_number, self.materiel_texture.index)


class StatusChange(models.Model):
    bidform=models.ForeignKey(BidForm,verbose_name=u"标单")
    original_status=models.ForeignKey(BidFormStatus,related_name="original",null=False,verbose_name=u"原状态")
    new_status=models.ForeignKey(BidFormStatus,null=False,related_name="new",verbose_name=u"新状态")
    change_user=models.ForeignKey(User,null=False,verbose_name=u"更改用户")
    change_time=models.DateTimeField(null=False,default = datetime.datetime.now(),verbose_name=u"更改时间")
    normal_change=models.BooleanField(default=True,verbose_name=u"是否正常更改")
    class Meta:
        verbose_name = u"状态更改"
        verbose_name_plural = u"状态更改"
    def __unicode__(self):
        return "from %s to %s"%(self.original_status.__unicode__(),self.new_status.__unicode__())

class StatusChangeReason(models.Model):
    status_change = models.OneToOneField(StatusChange,verbose_name=u"状态改变")
    reason = models.CharField(max_length = 1000, blank = True,null = True , verbose_name = u"回溯原因")
    class Meta:
        verbose_name = u"状态回溯原因"
        verbose_name_plural = u"状态回溯原因"
    def __unicode__(self):
        return "from %s to  %s" % (self.status_change.original_status.__unicode__() , self.status_change.new_status.__unicode__())
