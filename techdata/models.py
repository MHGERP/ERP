#coding: utf=8
from django.db import models
from const.models import *
from django.contrib.auth.models import User
from users.models import Group
from purchasing.models import MaterielExecute
import settings

class WeldQuota(models.Model):
    order = models.ForeignKey(WorkOrder, verbose_name = u"所属工作令")
    weld_material = models.ForeignKey(Material, verbose_name = u"焊材")
    size = models.CharField(null = True, blank = True, max_length = 100, verbose_name = "规格")
    quota = models.FloatField(null = True, blank = True, verbose_name = "定额")
    remark = models.CharField(null = True, blank = True, max_length = 100, verbose_name = u"备注")
    stardard = models.CharField(null = True, blank = True, max_length = 100, verbose_name = u"执行标准")
    class Meta:
        verbose_name = u"焊材定额"
        verbose_name_plural = u"焊材定额"
    def __unicode__(self):
        return self.weld_material.name + "(%s)" % (self.size)
    

class ProcessingName(models.Model):
    name = models.CharField(blank = False, choices = PROCESSING_CHOICES, max_length = 10, verbose_name = u"工序简称")
    class Meta:
        verbose_name = u"工序名称"
        verbose_name_plural = u"工序名称"

    def __unicode__(self):
        return self.get_name_display()

class Processing(models.Model):
    materiel_belong = models.OneToOneField(Materiel, blank = False, verbose_name = u"所属物料")
    GX1 = models.ForeignKey(ProcessingName, blank = True, null = True, verbose_name = u"工序1", related_name = "GX1")
    GX2 = models.ForeignKey(ProcessingName, blank = True, null = True, verbose_name = u"工序2", related_name = "GX2")
    GX3 = models.ForeignKey(ProcessingName, blank = True, null = True, verbose_name = u"工序3", related_name = "GX3")
    GX4 = models.ForeignKey(ProcessingName, blank = True, null = True, verbose_name = u"工序4", related_name = "GX4")
    GX5 = models.ForeignKey(ProcessingName, blank = True, null = True, verbose_name = u"工序5", related_name = "GX5")
    GX6 = models.ForeignKey(ProcessingName, blank = True, null = True, verbose_name = u"工序6", related_name = "GX6")
    GX7 = models.ForeignKey(ProcessingName, blank = True, null = True, verbose_name = u"工序7", related_name = "GX7")
    GX8 = models.ForeignKey(ProcessingName, blank = True, null = True, verbose_name = u"工序8", related_name = "GX8")
    GX9 = models.ForeignKey(ProcessingName, blank = True, null = True, verbose_name = u"工序9", related_name = "GX9")
    GX10 = models.ForeignKey(ProcessingName, blank = True, null = True, verbose_name = u"工序10", related_name ="GX10")
    GX11 = models.ForeignKey(ProcessingName, blank = True, null = True, verbose_name = u"工序11", related_name = "GX11")
    GX12 = models.ForeignKey(ProcessingName, blank = True, null = True, verbose_name = u"工序12", related_name = "GX12")

    GS1 = models.CharField(max_length = 20, blank = True, null = True, verbose_name = u"工时1")
    GS2 = models.CharField(max_length = 20, blank = True, null = True, verbose_name = u"工时2")
    GS3 = models.CharField(max_length = 20, blank = True, null = True, verbose_name = u"工时3")
    GS4 = models.CharField(max_length = 20, blank = True, null = True, verbose_name = u"工时4")
    GS5 = models.CharField(max_length = 20, blank = True, null = True, verbose_name = u"工时5")
    GS6 = models.CharField(max_length = 20, blank = True, null = True, verbose_name = u"工时6")
    GS7 = models.CharField(max_length = 20, blank = True, null = True, verbose_name = u"工时7")
    GS8 = models.CharField(max_length = 20, blank = True, null = True, verbose_name = u"工时8")
    GS9 = models.CharField(max_length = 20, blank = True, null = True, verbose_name = u"工时9")
    GS10 = models.CharField(max_length = 20, blank = True, null = True, verbose_name = u"工时10")
    GS11 = models.CharField(max_length = 20, blank = True, null = True, verbose_name = u"工时11")
    GS12 = models.CharField(max_length = 20, blank = True, null = True, verbose_name = u"工时12")
    class Meta:
        verbose_name = u"工序路线"
        verbose_name_plural = u"工序路线"
    def __unicode__(self):
        return self.materiel_belong.name

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

class WeldCertification(models.Model):
    name = models.CharField(blank = False,max_length = 100, choices = WELD_CERTIFICATION, verbose_name = u"焊工持证项目")
    class Meta:
        verbose_name = u"焊工持证项目"
        verbose_name_plural = u"焊工持证项目"
    def __unicode__(self):
        return self.name

class ProcedureQualificationIndex(models.Model):
    name = models.CharField(blank = False, max_length = 100, choices = PROCEDURE_QUALIFICATION_INDEX, verbose_name = u"焊接工艺评定编号")
    class Meta:
        verbose_name = u"焊接工艺评定编号"
        verbose_name_plural = u"焊接工艺评定编号"
    def __unicode__(self):
        return self.name

class WeldJointTech(models.Model):
    order = models.OneToOneField(WorkOrder, verbose_name = u"所属工作令")
    index = models.CharField(blank = True, null = True, max_length = 50, verbose_name = u"编号")
    remark = models.CharField(blank = True, null = True,  max_length = 200, verbose_name = u"备注")
    checker = models.ForeignKey(User, blank = True, null = True, verbose_name = u"审核人", related_name = "weldjoint_checker")
    approver = models.ForeignKey(User, blank = True, null = True, verbose_name = u"批准人", related_name = "weldjoint_approver")
    class Meta:
        verbose_name = u"焊接接头工艺分析表"
        verbose_name_plural = u"焊接接头工艺分析表"
    def __unicode__(self):
        return self.index

class WeldJointTechDetail(models.Model):
    weld_joint = models.ForeignKey(WeldJointTech, verbose_name = u"焊接接头工艺分析表")
    joint_index = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"接头编号")
    bm_texture_1 = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"母材材质1")
    bm_specification_1 = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"母材规格1")
    bm_texture_2 = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"母材材质2")
    bm_specification_2 = models.CharField(blank = True, null = True, max_length = 100, verbose_name =  u"母材材质2")
    weld_method_1 = models.ForeignKey(WeldMethod,null = True, blank = True, verbose_name = u"焊接方法", related_name = u"joint_weld_method1")
    weld_method_2 = models.ForeignKey(WeldMethod, null = True, blank = True, verbose_name = u"焊接方法", related_name = u"joint_weld_method2")
    procedureQualification_index = models.ForeignKey(ProcedureQualificationIndex, blank = True, null = True,max_length = 100, verbose_name = u"焊接工艺评定编号")
    weld_certification = models.ManyToManyField(WeldCertification, blank = True, null = True, verbose_name = u"焊工持证项目", related_name = "weld_certification")
    remark = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"备注")
    is_save = models.BooleanField(default = False, verbose_name = u"是否保存")
    class Meta:
        verbose_name = u"焊接接头"
        verbose_name_plural = u"焊接接头"
    def __unicode__(self):
        return self.joint_index

class WeldPositionType(models.Model):
    name = models.CharField(max_length = 100, choices = WELD_POSITION_CHOICES, verbose_name = u"焊接位置名")
    class Meta:
        verbose_name = u"焊接位置"
        verbose_name_plural = u"焊接位置"
    def __unicode__(self):
        return self.get_name_display()

class WeldSeam(models.Model):
    materiel_belong = models.ForeignKey(Materiel, verbose_name = u"所属物料")
    weld_index = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"焊缝编号")
    weldseam_type = models.ForeignKey(WeldSeamType, verbose_name = u"焊缝类型")
    weld_position = models.ForeignKey(WeldPositionType, verbose_name = u"焊接位置")
    weld_method_1 = models.ForeignKey(WeldMethod, null = True, blank = True, verbose_name = u"焊接方法1", related_name = "weld_method_1")
    weld_method_2 = models.ForeignKey(WeldMethod, null = True, blank = True, verbose_name = u"焊接方法2", related_name = "weld_method_2")
    base_metal_1 = models.CharField(null = True, blank = True, max_length = 100, verbose_name = "母材材质1")
    base_metal_2 = models.CharField(null = True, blank = True, max_length = 100, verbose_name = "母材材质2")
    base_metal_thin_1 = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"母材厚度1")
    base_metal_thin_2 = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"母材厚度2")
    length = models.CharField(blank = False, max_length = 100, verbose_name = u"长度")
    weld_material_1 = models.ForeignKey(Material, blank = True, null = True, verbose_name = u"焊材1", related_name = "weld_material_1")
    thin_1 = models.CharField(max_length = 100, blank = True, null = True, verbose_name = u"焊材厚度1")
    size_1 = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"规格1")
    weight_1 = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"重量1")
    weld_material_2 = models.ForeignKey(Material, blank = True, null = True, verbose_name = u"焊材2", related_name = "weld_material_2")
    thin_2 = models.CharField(max_length = 100, blank = True, null = True, verbose_name = u"焊材厚度2")
    size_2 = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"规格2")
    weight_2 = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"重量2")
    remark = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"备注")
    
    weld_joint_detail = models.ForeignKey(WeldJointTechDetail, blank = True, null = True, verbose_name = u"焊接接头", on_delete = models.SET_NULL, related_name = "weld_joint_detail")
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
    file_index = models.CharField(max_length = 100, null = True, blank = True, verbose_name = u"文件编号")
    materiel_belong = models.ForeignKey(Materiel, verbose_name = u"所属零件")
    card_type = models.CharField(blank = False, max_length = 100, choices = TRANSFER_CARD_TYPE_CHOICES, verbose_name = u"流转卡类型")
    class Meta:
        verbose_name = u"流转卡"
        verbose_name_plural = u"流转卡"
    def __unicode__(self):
        if self.card_type == CYLIDER_TRANSFER_CARD:
            return "RH04-" + str(self.file_index)
        elif self.card_type == CAP_TRANSFER_CARD:
            return "RH03-" + str(self.file_index)

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

class HeatTreatmentTechCard(models.Model):
    file_index = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"文件编号")
    writer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"编制人", related_name = "heattreatcard_writer")
    write_date = models.DateField(blank = True, null = True, verbose_name = u"编制日期")

    reviewer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"审核人", related_name = "heattreatcard_reviewer")
    review_date = models.DateField(blank = True, null = True, verbose_name = u"审核日期")

    temperature_start = models.CharField(max_length = 20, null = True, blank = True, verbose_name = u"进炉温度")
    temperature_end = models.CharField(max_length = 20, null = True, blank = True, verbose_name = u"出炉温度")
    temperature_top = models.CharField(max_length = 20, null = True, blank = True, verbose_name = u"最高温度")
    temperature_up_speed = models.CharField(max_length = 20, null = True, blank = True, verbose_name = u"升温速率")
    temperature_down_speed = models.CharField(max_length = 20, null = True, blank = True, verbose_name = u"降温速率")
    time = models.CharField(max_length = 20, null = True, blank = True, verbose_name = u"保温时间")

    class Meta:
        verbose_name = u"热处理工艺卡"
        verbose_name_plural = u"热处理工艺卡"
    def __unicode__(self):
        return "RR01-" + str(self.file_index)

class HeatTreatmentMateriel(models.Model):
    materiel = models.ForeignKey(Materiel, verbose_name = u"零件")
    max_heattreat_thin = models.CharField(max_length = 20, null = True, blank = True, verbose_name  = u"最大热处理厚度")
    heat_test = models.CharField(max_length = 100, null = True, blank = True, verbose_name = u"热处理检验")
    operator = models.ForeignKey(User, blank = True, null = True, verbose_name = u"操作者")
    test_result = models.CharField(max_length = 100, null = True, blank = True, verbose_name = u"检验结果")
    card_belong = models.ForeignKey(HeatTreatmentTechCard, null = True, blank = True, verbose_name = u"所属工艺卡")
    class Meta:
        verbose_name = u"热处理件"
        verbose_name_plural = u"热处理件"
    def __unicode__(self):
        return unicode(self.materiel)

class HeatTreatmentArrangement(models.Model):
    file_index = models.CharField(blank = True, null = True, max_length = 100, verbose_name = u"文件编号")
    card_belong = models.OneToOneField(HeatTreatmentTechCard, verbose_name = u"所属工艺卡")

    writer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"编制人", related_name = "heattreatarrange_writer")
    write_date = models.DateField(blank = True, null = True, verbose_name = u"编制日期")

    reviewer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"审核人", related_name = "heattreatarrange_reviewer")
    review_date = models.DateField(blank = True, null = True, verbose_name = u"审核日期")
    
    file_obj = models.FileField(upload_to = settings.PROCESS_FILE_PATH + "/%Y/%m/%d", verbose_name = u"布置图")
    class Meta:
        verbose_name = u"热处理测温点布置"
        verbose_name_plural = u"热处理测温点布置"
    def __unicode__(self):
        return "RR02-" + str(self.file_index)

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
    order = models.ForeignKey(WorkOrder, blank = True, null = True, verbose_name=u"所属工作令")
    detail = models.CharField(max_length = 100, blank = True, null = True, verbose_name = u"详细内容")
    sentDepartment = models.ForeignKey(Group, blank = False, null = False, verbose_name = u"下发部门")
    planCompleteDate = models.DateField(blank = False, null = False, verbose_name = u"计划完成时间")
    month = models.IntegerField(blank = True, null = False, verbose_name = u"所属月份")
    year = models.IntegerField(blank = True, null = False, verbose_name = u"所属年份")
    class Meta:
        verbose_name = u"技术准备计划"
        verbose_name_plural = u"技术准备计划"
    def __unicode__(self):
        return self.order.order_index + "(%s)" % self.detail

class WeldQuotaPageMark(models.Model):
    order = models.OneToOneField(WorkOrder, verbose_name = u"所属工作令")
    writer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"编制人", related_name = "weld_quota_writer")
    write_date = models.DateField(blank = True, null = True, verbose_name = u"编制日期")
    reviewer = models.ForeignKey(User, blank = True, null = True, verbose_name = u"审核人", related_name = "weld_quota_reviewer")
    review_date = models.DateField(blank = True, null = True, verbose_name = u"审核日期")
    class Meta:
        verbose_name = u"焊材明细签章"
        verbose_name_plural = u"焊材明细签章"
    def __unicode__(self):
        return self.order.order_index


class ConnectOrientation(models.Model):
    order = models.ForeignKey(WorkOrder, verbose_name = u"所属工作令")
    name = models.CharField(max_length = 100, blank = False, verbose_name = u"文件名称")
    file_obj = models.FileField(upload_to = settings.PROCESS_FILE_PATH + "/%Y/%m/%d", verbose_name = u"程序")
    upload_date = models.DateTimeField(null = True, blank = True, verbose_name = u"上传时间")
    file_size = models.CharField(max_length = 50, blank = True, null = True, default = None, verbose_name = "文件大小")
    file_type = models.CharField(max_length = 50, blank = True, null = True, default = None, verbose_name = "文件类型")
    class Meta:
        verbose_name = u"管口方位图"
        verbose_name_plural = u"管口方位图"
    def __unicode__(self):
        return self.name
