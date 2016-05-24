# coding: UTF-8
from const import *
import datetime
from django.db import models
from const.utility import make_uuid

from const.models import BidFormStatus,Materiel,Material, WorkOrder, OrderFormStatus, ImplementClassChoices,SubWorkOrder, InventoryType
from django.contrib.auth.models import User
import settings
# Create your models here.

class MaterielCopy(Materiel):
    relate_material=models.ForeignKey('self',null=True,blank=True)
    orgin_materiel=models.ForeignKey(Materiel,null=True,related_name="orgin_materiel",blank=True)
    work_order=models.CharField(blank=True,null=True,max_length=100,verbose_name=u"工作令号")
    sub_workorder=models.ForeignKey(SubWorkOrder,blank=True,null=True,verbose_name=u"子工作令")
    inventory_type = models.ForeignKey(InventoryType, blank = True, null = True, verbose_name = "明细表类型")
    batch_number=models.CharField(blank=True,null=True,max_length=50,verbose_name=u"炉批号")
    quality_number=models.CharField(blank=True,null=True,max_length=50,verbose_name=u"材质编号")
    delivery_time=models.CharField(blank=True,null=True,max_length=50,verbose_name=u"交货期")
    material_classify=models.CharField(blank=True,null=True,max_length=50,verbose_name=u"材料分类")
    is_finish=models.BooleanField(default = False, verbose_name = u"是否结束")
    class Meta:
        verbose_name = u"伪物料"
        verbose_name_plural = u"伪物料"
    def __unicode__(self):
        return "%s  %s"%(self.name,self.specification)

class CommentStatus(models.Model):
    form_type=models.IntegerField(choices=BID_APPLY_TYPE_CHOICES,blank=True,null=True,verbose_name=u"表单类型")
    status=models.IntegerField(choices=COMMENT_STATUS_CHOICES,unique=True,verbose_name=u"表单状态")
    next_status=models.ForeignKey('self',null=True,blank=True)
    class Meta:
        verbose_name = u"招标申请状态"
        verbose_name_plural = u"招标申请状态"
    def __unicode__(self):
        return self.get_status_display()

class MaterielExecute(models.Model):
    document_number = models.CharField(max_length = 100, null = True, blank = False, unique = True, verbose_name = u"单据编号")
    document_lister = models.ForeignKey(User, blank = False, verbose_name = u"制表人")
    date = models.DateField(blank = False, null = False, verbose_name = u"制表日期")
    materiel_choice = models.CharField(blank=False, max_length = 20, choices=MATERIEL_CHOICE, verbose_name=u"材料选择")
    is_save = models.BooleanField(blank=False, verbose_name=u"是否已保存")
    tech_feedback = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"工艺反馈")
    tech_requirement=models.CharField(max_length=5000,blank=True,null=True)
    class Meta:
        verbose_name = u"材料执行表"
        verbose_name_plural = u"材料执行表"
    def __unicode__(self):
        return '%s' % self.document_number

class OrderForm(models.Model):
    order_id = models.CharField(unique = True, max_length = 20, blank = False, verbose_name = u"订购单编号")
    create_time = models.DateTimeField(null = True,verbose_name = u"创建日期")
    establishment_time = models.DateTimeField(null = True, verbose_name = u"编制日期")
    audit_time=models.DateTimeField(blank=True,null=True,verbose_name=u"审核日期")
    approved_time=models.DateTimeField(blank=True,null=True,verbose_name=u"批准日期")
    order_status = models.ForeignKey(OrderFormStatus, null = False, verbose_name = u"订购单状态")
    establishment_user=models.ForeignKey(User,verbose_name=u"编制人",related_name="establishment_user",null=True,blank=True)
    chief=models.ForeignKey(User,verbose_name=u"外采科长",related_name="chief_user",null=True,blank=True)
    approve_user=models.ForeignKey(User,verbose_name=u"审批人",related_name="approve_user",null=True,blank=True)
    tech_requirement=models.TextField(max_length=5000,blank=True,null=True)
    order_mod=models.IntegerField(default=0,verbose_name=u"标单类型")
    work_order=models.CharField(blank=True,null=True,max_length=100,verbose_name=u"工作令号")
    number=models.CharField(blank=True,null=True,max_length=100,verbose_name=u"编号")
    revised_id=models.CharField(blank=True,null=True,max_length=100,verbose_name=u"修订号")
    class Meta:
        verbose_name = u"订购单"
        verbose_name_plural = u"订购单"
    def __unicode__(self):
        return self.order_id

class BidForm(models.Model):
    order_form=models.ForeignKey(OrderForm,null=True,verbose_name=u'对应订购单')
    bid_id=models.CharField(unique=True,max_length=20,blank=False,verbose_name=u"标单编号")
    create_time=models.DateTimeField(blank=True,null=True,verbose_name=u"创建日期")
    establishment_time=models.DateTimeField(blank=True,null=True,verbose_name=u"编制日期")
    audit_time=models.DateTimeField(blank=True,null=True,verbose_name=u"审核日期")
    approved_time=models.DateTimeField(blank=True,null=True,verbose_name=u"批准日期")
    bid_status=models.ForeignKey(BidFormStatus,null=False,verbose_name=u"标单状态")
    contract_id = models.CharField(max_length=50, blank=True, default=make_uuid, verbose_name=u"合同编号")
    contract_amount = models.IntegerField(default=0,verbose_name=u"合同金额")
    billing_amount = models.IntegerField(default=0,verbose_name=u"开票金额")
    bid_mod = models.IntegerField(default=0,verbose_name=u"招标申请类型")
    class Meta:
        verbose_name = u"标单"
        verbose_name_plural = u"标单"
    def __unicode__(self):
        return '%s'% (self.bid_id)
    def prepaid_amount(self):
        return reduce(lambda x,y: x + y, [ item.amount for item in self.contractdetail_set.all()] , 0)
    def payable_amount(self):
        return self.billing_amount - self.prepaid_amount()
    def supplier_select(self):
        return ",".join([ item.supplier.supplier_name for item in self.supplierselect_set.all()])

class ContractDetail(models.Model):
    user = models.ForeignKey(User, blank = False)
    submit_date = models.DateField(blank=True,null=True,default=lambda: datetime.datetime.today(),verbose_name=u"提交日期")
    amount = models.IntegerField(verbose_name=u"金额")
    bidform = models.ForeignKey(BidForm, null = False, verbose_name = u"标单")
    class Meta:
        verbose_name = u"合同金额明细"
        verbose_name_plural = u"合同金额明细"
    def __unicode__(self):
        return '%s'% (self.amount)

class CommentBase(models.Model):
    user = models.ForeignKey(User, blank = False)
    comment = models.CharField(max_length=400,blank=False,verbose_name=u"审批意见")
    submit_date=models.DateField(blank=True,null=True,default=lambda: datetime.datetime.today(),verbose_name=u"提交日期")
    class Meta:
        abstract=True
        verbose_name=u"评审意见基本"

class BidComment(CommentBase):
    bid = models.ForeignKey(BidForm, blank = False)
    user_title=models.IntegerField(choices=COMMENT_USER_CHOICE,verbose_name=u"审批人属性")
    class Meta:
        verbose_name = u"标单评审意见"
        verbose_name_plural = u"标单评审意见"
    def __unicode__(self):
        return '%s'% (self.id)


class MaterielFormConnection(models.Model):
    materiel = models.OneToOneField(MaterielCopy, blank = False, verbose_name = u"物料")
    order_form = models.ForeignKey(OrderForm, blank = True, null = True, verbose_name = u"订购单")
    bid_form = models.ForeignKey(BidForm, blank = True, null = True, verbose_name = u"标单")
    count = models.CharField(blank = True, null = True, max_length = 20, verbose_name = u"需求数量")
    purchasing = models.CharField(blank = True, null = True, max_length = 20, verbose_name = u"采购")
    class Meta:
        verbose_name = u"物料——采购——关联表"
        verbose_name_plural = u"物料——采购——关联表"
    def __unicode__(self):
        return "%s %s"%(self.materiel.name,self.materiel.specification)



class bidApply(models.Model):
    apply_id = models.CharField(null=True,blank=True,unique=True, max_length=50, default="", verbose_name=u"标单申请编号")
    apply_company = models.CharField(null=True, max_length=40, verbose_name=u"申请单位")
    demand_company = models.CharField(null=True, max_length=40, verbose_name=u"需求单位")
    amount = models.IntegerField(default=0,verbose_name=u"数量")
    work_order = models.CharField(max_length=100,null=True,verbose_name=u"工作令")
    bid_project = models.CharField(null=True, max_length=40, verbose_name=u"拟招(议)项目")
    bid_date = models.DateTimeField(null=True, verbose_name=u"拟招(议)标时间")
    special_model = models.CharField(null=True, blank=True,max_length=40, verbose_name=u"规格、型号")
    core_part = models.BooleanField(verbose_name="是否为核心件", default = False)

    bid = models.OneToOneField(BidForm)
    project_category = models.CharField(null=True, blank=True, max_length=40, verbose_name=u"项目类别")
    bid_datetime = models.DateTimeField(null=True, blank=True, default=lambda: datetime.datetime.today(), verbose_name=u"招(议)标时间")
    bid_delivery_date = models.DateTimeField(null=True, blank=True, default=lambda: datetime.datetime.today(), verbose_name=u"标书递送时间")
    place = models.CharField(null=True, blank=True, max_length=40, verbose_name=u"地点")
    status=models.ForeignKey(CommentStatus,verbose_name=u"招标申请表状态")
    try:
        default_status = ImplementClassChoices.objects.get(category = 0).id
    except:
        default_status = 1
    implement_class = models.ForeignKey(ImplementClassChoices, blank=False, default=default_status, verbose_name=u"实施类别")

    class Meta:
        verbose_name = u"标单申请表"

    def __unicode__(self):
        return '%s'% (self.bid.bid_id)

class qualityPriceCard(models.Model):
    bid = models.OneToOneField(BidForm, blank = False)
    apply_id = models.CharField(max_length=20, blank=True,null=True, verbose_name=u"标单申请编号")
    apply_company = models.CharField(null=True, max_length=40, verbose_name=u"申请单位")
    demand_company = models.CharField(null=True,blank=True, max_length=40, verbose_name=u"需求单位")
    work_order = models.CharField(max_length=50,null=True,blank=True,verbose_name=u"工作令")
    amount = models.IntegerField(null=True,blank=True,verbose_name=u"数量")
    unit = models.CharField(null=True, max_length=40, verbose_name=u"单位")
    content = models.CharField(null=True, max_length=40, verbose_name=u"内容")
    material = models.CharField(null=True, max_length=40, verbose_name=u"材质")
    delivery_period = models.CharField(null=True, max_length=40, verbose_name=u"交货期")
    status=models.ForeignKey(CommentStatus,verbose_name=u"招标申请表状态")
    class Meta:
        verbose_name = u"比质比价卡"

    def __unicode__(self):
        return '%s'% (self.bid.bid_id)
class SupplierCheck(models.Model):
    bid=models.OneToOneField(BidForm,blank=False)
    apply_company = models.CharField(null=True,blank=True, max_length=40, verbose_name=u"申请单位")
    apply_date = models.DateTimeField(null=True, blank=True,verbose_name=u"申请日期")
    bid_project = models.CharField(null=True, max_length=40,blank=True, verbose_name=u"项目名称")
    price_estimate = models.CharField(null=True, max_length=40, blank=True,verbose_name=u"估算价格")
    base_situation = models.CharField(null=True,blank=True, max_length=100, verbose_name=u"招（议）标项目基本情况")
    status=models.ForeignKey(CommentStatus,verbose_name=u"招标申请表状态")
    class Meta:
        verbose_name = u"供应商审核"
        verbose_name_plural = u"供应商审核"
    def __unicode__(self):
        return '%s'% (self.bid.bid_id)

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
    material = models.ForeignKey(MaterielCopy,verbose_name=u"材料")
    check_pass=models.BooleanField(default=False,verbose_name=u"是否通过")
    class Meta:
        verbose_name = u"到货检验"
        verbose_name_plural = u"到货检验"

    def __unicode__(self):
        return '%s(%s)' % (self.bidform.bid_id,self.material.name)



class MaterielPurchasingStatus(models.Model):
    materiel = models.OneToOneField(MaterielCopy)
    add_to_detail = models.BooleanField(default = False)
    class Meta:
        verbose_name = u"物料采购状态"
        verbose_name_plural = u"物料采购状态"
    def __unicode__(self):
       return '%s  %s'%(self.materiel.name,self.materiel.specification)

class SupplierSelect(models.Model):
    bidform=models.ForeignKey(BidForm,blank=False,verbose_name=u"标单")
    supplier=models.ForeignKey(Supplier,blank=False,verbose_name=u"供应商")
    A=models.BooleanField(blank=True,default=False,verbose_name="A")
    B=models.BooleanField(blank=True,default=False,verbose_name="B")
    C=models.IntegerField(choices=SupplierCChoices,blank=True,null=True,verbose_name="C")
    D=models.BooleanField(blank=True,default=False,verbose_name="D")
    E=models.BooleanField(blank=True,default=False,verbose_name="E")
    F=models.BooleanField(blank=True,default=False,verbose_name="F")
    G=models.BooleanField(blank=True,default=False,verbose_name="G")
    sphere=models.CharField(max_length=40,blank=True,null=True,verbose_name=u"认定业务范围")
    supplier_code=models.CharField(max_length=40,blank=True,null=True,verbose_name=u"供方代码")
    price=models.CharField(max_length=40,blank=True,null=True,verbose_name=u"价格")
    ability_situation=models.CharField(max_length=200,blank=True,null=True,verbose_name=u"厂家协作能力质量情况及业绩")
    delivery_payment=models.CharField(max_length=40,blank=True,null=True,verbose_name=u"交货及支付条件")
    class Meta:
        verbose_name = u"供应商选择"
        verbose_name_plural = u"供应商选择"
        unique_together = (("bidform", "supplier", ), )
    def __unicode__(self):
        return "%s select %s" % (self.bidform.bid_id, self.supplier.supplier_name)

class MaterialSubApply(models.Model):
    receipts_code = models.CharField(max_length = 100, unique = True, blank = False ,null = True, verbose_name = u"单据编号")
    pic_code =  models.CharField(max_length = 100, blank = False , null = True, verbose_name = u"图号")
    work_order = models.CharField(max_length=50,verbose_name = u"工作令" , blank = True , null = True)
    production_name = models.CharField(max_length=50,verbose_name = u"产品名称" , blank = True , null = True)
    reasons = models.CharField(max_length = 1000,blank = True, null = True, verbose_name = u"代用原因和理由")
    proposer = models.ForeignKey(User,verbose_name = u"申请人",blank = True)
    status=models.ForeignKey(CommentStatus,verbose_name=u"招标申请表状态")
    class Meta:
        verbose_name = u"材料代用申请单"
        verbose_name_plural = u"材料代用申请单"
    def __unicode__(self):
        return "%s" % (self.receipts_code)

class SubApplyComment(CommentBase):
    subapply=models.ForeignKey(MaterialSubApply,blank=False)
    user_title=models.IntegerField(choices=COMMENT_USER_CHOICE,verbose_name=u"审批人属性")
    class Meta:
        verbose_name = u"材料代用评审意见"
        verbose_name_plural = u"材料代用评审意见"
    def __unicode__(self):
        return '%s'% (self.id)
    

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
        return "%s(%s)" % (self.sub_apply.receipts_code,self.mat_pic_code)

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

class MaterielExecuteDetail(models.Model):
    materiel_execute = models.ForeignKey(MaterielExecute, null = True, blank = True, verbose_name = u"材料执行")
    materiel=models.ForeignKey(MaterielCopy,verbose_name=u"物料")
    batch_number = models.CharField(max_length = 50, null = True, blank = True, verbose_name = u"出厂批号")
    quota = models.CharField(max_length = 50, null = True, blank = True, verbose_name = u"定额")
    part = models.CharField(max_length = 50, null = True, blank = True, verbose_name = u"零件")
    oddments = models.CharField(max_length = 50, null = True, blank = True, verbose_name = u"余料")
    remark = models.CharField(max_length = 200, null = True, blank = True, verbose_name = u"备注")
    class Meta:
        verbose_name = u"材料执行表详细"
        verbose_name_plural = u"材料执行表详细"
    def __unicode__(self):
        return '%s' % (self.materiel.name)

class BidAcceptance(models.Model):
    bid=models.OneToOneField(BidForm,verbose_name=u"标单")
    document_id=models.CharField(max_length = 50,blank=True,null=True,verbose_name=u"标书编号")
    apply_company = models.CharField(null=True, max_length=40, verbose_name=u"招（议）标单位")
    apply_content = models.CharField(null=True, max_length=40, verbose_name=u"招（议）标内容")
    amount=models.CharField(null=True, max_length=40, verbose_name=u"数量")
    accept_date = models.DateTimeField(null=True, blank=True,verbose_name=u"中标日期")
    accept_money=models.CharField(null=True, blank=True,max_length=40, verbose_name=u"中标金额")
    accept_supplier=models.ForeignKey(Supplier,null=True,blank=True,verbose_name=u"中标单位")
    contact_people=models.CharField(null=True, blank=True,max_length=40, verbose_name=u"联系人")
    contact_tel=models.CharField(null=True, blank=True,max_length=40, verbose_name=u"联系电话")
    class Meta:
        verbose_name = u"中标通知书"
        verbose_name_plural = u"中标通知书"
    def __unicode__(self):
        return '%s' % (self.bid.bid_id)

class QuotingPrice(models.Model):
    inventory_type = models.ForeignKey(InventoryType, verbose_name=u"库存")
    nameorspacification = models.CharField(max_length=50,blank=True,null=True,verbose_name=u"规格及名称")
    material_mark = models.CharField(max_length=50,blank=True,null=True,verbose_name=u"材质或牌号")
    per_fee = models.CharField(max_length=50,blank=True,null=True,verbose_name=u"单价")
    unit = models.CharField(max_length=50,blank=True,null=True,verbose_name=u"单位")
    the_supplier=models.ForeignKey(Supplier,verbose_name=u"供应商")
    class Meta:
        verbose_name = u"报价单"
        verbose_name_plural = u"报价单"
    def __unicode__(self):
        return '%s' % (self.per_fee)
