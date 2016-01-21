#coding: utf=8
from const import PROCESSING_CHOICES, CIRCULATION_CHOICES, NONDESTRUCTIVE_INSPECTION_TYPE, TRANSFER_CARD_TYPE_CHOICES
from django.db import models
from const.models import Materiel, Material, WorkOrder
from django.contrib.auth.models import User
from users.models import Group
from purchasing.models import MaterielExecute
import settings

class Processing(models.Model):
    materiel_belong = models.ForeignKey(Materiel, verbose_name = u"所属物料")
    name = models.CharField(blank = False, choices = PROCESSING_CHOICES, max_length = 10, verbose_name = u"工序名")
    next_processing = models.ForeignKey('self', null = True, blank = True, verbose_name = u"下一工序")
    is_first_processing = models.BooleanField(blank = False, default = False, verbose_name = u"首道工序")
    instruction = models.CharField(blank = True, null = True, max_length = 10, verbose_name = u"说明")
    index = models.CharField(blank = True, null = True, max_length = 10, verbose_name = u"工号")
    hour = models.FloatField(blank = True, null = True, verbose_name = u"工时")

    technical_requirement = models.CharField(blank = True, null = True, max_length = 1000, verbose_name = u"工艺过程及技术要求")
    operator = models.ForeignKey(User, blank = True, null = True, verbose_name = u"操作者", related_name = "process_operator")
    operate_date = models.DateField(blank = True, null = True, verbose_name = u"操作时间")
    inspector = models.ForeignKey(User, blank = True, null = True, verbose_name = u"检查者", related_name = "process_inspector")
    inspect_date = models.DateField(blank = True, null = True, verbose_name = u"检查时间")
    class Meta:
        verbose_name = u"工序"
        verbose_name_plural = u"工序"

    def __unicode__(self):
        return self.materiel_belong.name + "(%s)" % self.get_name_display()

class ProcessReview(models.Model):
    materiel = models.ForeignKey(Materiel, verbose_name = u"零件")
    problem_statement = models.CharField(blank = True, null = True, max_length = 200, verbose_name = u"存在问题")
    advice_statement = models.CharField(blank = True, null = True, max_length = 200, verbose_name = u"改进建议")
    class Meta:
        verbose_name = u"工艺性审查表"
        verbose_name_plural = u"工艺性审查表"
    def __unicode__(self):
        return self.materiel.name

class CirculationName(models.Model):
    name = models.CharField(blank = False, max_length = 10, choices = CIRCULATION_CHOICES, verbose_name = u"流转简称")
    full_name = models.CharField(blank = True, null = True, max_length = 10, verbose_name = u"流转名称全称")
    class Meta:
        verbose_name = u"流转名称"
        verbose_name_plural = u"流转名称"
    def __unicode__(self):
        return self.get_name_display()

class CirculationRoute(models.Model):
    materiel_belong = models.OneToOneField(Materiel, blank = False, verbose_name = u"所属物料")
    L1 = models.ForeignKey(CirculationName, blank = True, null = True, verbose_name = u"L1", related_name = "L1")
    L2 = models.ForeignKey(CirculationName, blank = True, null = True, verbose_name = u"L2", related_name = "L2")
    L3 = models.ForeignKey(CirculationName, blank = True, null = True, verbose_name = u"L3", related_name = "L3")
    L4 = models.ForeignKey(CirculationName, blank = True, null = True, verbose_name = u"L4", related_name = "L4")
    L5 = models.ForeignKey(CirculationName, blank = True, null = True, verbose_name = u"L5", related_name = "L5")
    L6 = models.ForeignKey(CirculationName, blank = True, null = True, verbose_name = u"L6", related_name = "L6")
    L7 = models.ForeignKey(CirculationName, blank = True, null = True, verbose_name = u"L7", related_name = "L7")
    L8 = models.ForeignKey(CirculationName, blank = True, null = True, verbose_name = u"L8", related_name = "L8")
    L9 = models.ForeignKey(CirculationName, blank = True, null = True, verbose_name = u"L9", related_name = "L9")
    L10 = models.ForeignKey(CirculationName, blank = True, null = True, verbose_name = u"L10", related_name = "L10")
    class Meta:
        verbose_name = u"流转路线"
        verbose_name_plural = u"流转路线"
    def __unicode__(self):
        return self.materiel_belong.name

class WeldSeamType(models.Model):
    name = models.CharField(blank = False, max_length = 100, verbose_name = u"类型名")
    class Meta:
        verbose_name = u"焊缝类型"
        verbose_name_plural = u"焊缝类型"
    def __unicode__(self):
        return self.name

class WeldMethod(models.Model):
    name = models.CharField(blank = False, max_length = 100, verbose_name = u"方法名")
    class Meta:
        verbose_name = u"焊接方法"
        verbose_name_plural = u"焊接方法"
    def __unicode__(self):
        return self.name


class NondestructiveInspection(models.Model):
    name = models.CharField(blank = False, choices = NONDESTRUCTIVE_INSPECTION_TYPE, max_length = 20, verbose_name = u"探伤种类名")
    class Meta:
        verbose_name = u"无损探伤"
        verbose_name_plural = u"无损探伤"
    def __unicode__(self):
        return self.name

class WeldSeam(models.Model):
    materiel_belong = models.ForeignKey(Materiel, verbose_name = u"所属物料")
    weld_index = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"焊缝编号")
    weldseam_type = models.ForeignKey(WeldSeamType, verbose_name = u"焊缝类型")
    weld_method = models.ForeignKey(WeldMethod, verbose_name = u"焊接方法")
    base_metal_thin_1 = models.CharField(blank = False, max_length = 100, verbose_name = u"母材厚度1")
    base_metal_thin_2 = models.CharField(blank = False, max_length = 100, verbose_name = u"母材厚度2")
    length = models.CharField(blank = False, max_length = 100, verbose_name = u"长度")
    weld_material_1 = models.ForeignKey(Material, blank = True, null = True, verbose_name = u"焊材1", related_name = "weld_material_1")
    size_1 = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"规格1")
    weight_1 = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"重量1")
    weld_material_2 = models.ForeignKey(Material, blank = True, null = True, verbose_name = u"焊材2", related_name = "weld_material_2")
    size_2 = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"规格2")
    weight_2 = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"重量2")
    remark = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"备注")

    groove_inspction = models.ManyToManyField(NondestructiveInspection, blank = True, null = True, verbose_name = u"坡口探伤", related_name = "groove_inspction")
    welded_status_inspection = models.ManyToManyField(NondestructiveInspection, blank = True, null = True, verbose_name = u"焊态探伤", related_name = "welded_status_inspection")
    heat_treatment_inspection = models.ManyToManyField(NondestructiveInspection, blank = True, null = True, verbose_name = u"热处理后探伤", related_name = "heat_treatment_inspection")
    pressure_test_inspection = models.ManyToManyField(NondestructiveInspection, blank = True, null = True, verbose_name = u"试压后探伤", related_name = "pressure_test_inspection")

    class Meta:
        verbose_name = u"焊缝"
        verbose_name_plural = u"焊缝"
    def __unicode__(self):
        return self.materiel_belong.name   

class WeldListPageMark(models.Model):
    order = models.OneToOneField(WorkOrder, verbose_name = u"所属工作令")
    writer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"编制人", related_name = "weld_list_writer")
    write_date = models.DateField(blank = True, null = True, verbose_name = u"编制日期")
    reviewer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"审核人", related_name = "weld_list_reviewer")
    review_date = models.DateField(blank = True, null = True, verbose_name = u"审核日期")
    class Meta:
        verbose_name = u"焊缝明细签章"
        verbose_name_plural = u"焊缝明细签章"
    def __unicode__(self):
        return self.order.order_index

class TransferCard(models.Model):
    materiel_belong = models.ForeignKey(Materiel, verbose_name = u"所属零件")
    card_type = models.CharField(blank = False, max_length = 100, choices = TRANSFER_CARD_TYPE_CHOICES, verbose_name = u"流转卡类型")

    class Meta:
        verbose_name = u"流转卡"
        verbose_name_plural = u"流转卡"
    def __unicode__(self):
        return self.materiel_belong.name

class TransferCardMark(models.Model):
    card = models.OneToOneField(TransferCard, verbose_name = u"所属流转卡")

    writer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"编制人", related_name = "transfercard_writer")
    write_date = models.DateField(blank = True, null = True, verbose_name = u"编制日期")

    reviewer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"审核人", related_name = "transfercard_reviewer")
    review_date = models.DateField(blank = True, null = True, verbose_name = u"审核日期")

    proofreader = models.ForeignKey(User, blank = True, null = True, verbose_name = u"校对人", related_name = "transfercard_proofreader")
    proofread_date = models.DateField(blank = True, null = True, verbose_name = u"校对日期")

    approver = models.ForeignKey(User, blank = True, null = True, verbose_name = u"批准人", related_name = "transfercard_approver")
    approve_date = models.DateField(blank = True, null = True, verbose_name = u"批准日期")

    class Meta:
        verbose_name = u"流转卡签章"
        verbose_name_plural = u"流转卡签章"
    def __unicode__(self):
        return unicode(self.card)


class ProcessBOMPageMark(models.Model):
    order = models.OneToOneField(WorkOrder, verbose_name = u"所属工作令")
    
    writer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"工艺员", related_name = "processBOM_writer")
    write_date = models.DateField(blank = True, null = True, verbose_name = u"编制日期")

    quota_agent = models.ForeignKey(User, blank = True, null = True, verbose_name = u"定额员", related_name = "processBOM_quota_agent")
    quota_date = models.DateField(blank = True, null = True, verbose_name = u"定额日期")

    proofreader = models.ForeignKey(User, blank = True, null = True, verbose_name = u"校对人", related_name = "processBOM_proofreader")
    proofread_date = models.DateField(blank = True, null = True, verbose_name = u"校对日期")

    statistician = models.ForeignKey(User, blank = True, null = True, verbose_name = u"统计员", related_name = "processBOM_statistician")
    statistic_date = models.DateField(blank = True, null = True, verbose_name = u"统计日期")

    class Meta:
        verbose_name = u"工艺库签章"
        verbose_name_plural = u"工艺库签章"
    def __unicode__(self):
        return unicode(self.order)

class Program(models.Model):
    execute = models.ForeignKey(MaterielExecute, verbose_name = u"所属执行表")
    name = models.CharField(max_length = 100, blank = False, verbose_name = u"文件名称")
    file_obj = models.FileField(upload_to = settings.PROCESS_FILE_PATH + "/%Y/%m/%d", verbose_name = u"程序")
    upload_date = models.DateTimeField(null = True, blank = True, verbose_name = u"上传时间")
    file_size = models.CharField(max_length = 50, blank = True, null = True, default = None, verbose_name = "文件大小")
    file_type = models.CharField(max_length = 50, blank = True, null = True, default = None, verbose_name = "文件类型")
    class Meta:
        verbose_name = u"编程套料图"
        verbose_name_plural = u"编程套料图"
    def __unicode__(self):
        return self.name

class BoxOutBoughtMark(models.Model):
    order = models.OneToOneField(WorkOrder, verbose_name = u"所属工作令")
    writer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"编制人", related_name = "box_outbought_writer")
    write_date = models.DateField(blank = True, null = True, verbose_name = u"编制日期")
    reviewer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"审核人", related_name = "box_outbought_reviewer")
    review_date = models.DateField(blank = True, null = True, verbose_name = u"审核日期")
    class Meta:
        verbose_name = u"装箱外构件明细签章"
        verbose_name_plural = u"装箱外构件明细签章"
    def __unicode__(self):
        return self.order.order_index


class DesignBOMMark(models.Model):
    order = models.OneToOneField(WorkOrder, verbose_name = u"所属工作令")
    writer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"编制人", related_name = "designBOM_writer")
    write_date = models.DateField(blank = True, null = True, verbose_name = u"编制日期")
    reviewer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"审核人", related_name = "designBOM_reviewer")
    review_date = models.DateField(blank = True, null = True, verbose_name = u"审核日期")
    class Meta:
        verbose_name = u"设计库签章"
        verbose_name_plural = u"设计库签章"
    def __unicode__(self):
        return self.order.order_index

class TechPlan(models.Model):
    order = models.ForeignKey(WorkOrder, verbose_name=u"所属工作令")
    detail = models.CharField(max_length = 100, blank = True, null = True, verbose_name = u"详细内容")
    sentDepartment = models.ForeignKey(Group, blank = False, null = False, verbose_name = u"下发部门")
    planCompleteDate = models.DateField(blank = False, null = False, verbose_name = u"计划完成时间")
    class Meta:
        verbose_name = u"技术准备计划"
        verbose_name_plural = u"技术准备计划"
    def __unicode__(self):
        return self.order.order_index + "(%s)" % self.detail
