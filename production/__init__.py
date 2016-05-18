# coding=utf-8

TASK_ALLOCATION_STATUS_CHOICES = (
 ("",u"任务分配状态"),
 (1,u"未分配"),
 (0,u"已分配"),
)

TASK_CONFIRM_STATUS_CHOICES = (
  ("",u"任务完成状态"),
  (1,u"未完成"),
  (0,u"已完成"),
)

TASK_PLAN_STATUS_CHOICES = (
    ("",u"任务计划状态"),
    (1,u"未完成"),
    (0,u"已完成")
)

"""
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

class AuxiliaryToolApplyCard(models.Model):
    create_time=models.DateField(verbose_name=u'申请时间',auto_now_add=True)
    department = models.CharField(verbose_name=u"领用单位",max_length=50,blank=True,null=True)
    applycard_code = models.CharField(verbose_name=u"料单编号",max_length=20,blank=True,null=True)
    apply_storelist=models.ForeignKey(AuxiliaryToolStoreList,verbose_name=u'申请材料',blank=False,null=True,related_name="auap_apply_storelist")
    apply_quantity=models.IntegerField(verbose_name=u'申请数量',blank=False)
    actual_storelist = models.ForeignKey(AuxiliaryToolStoreList,verbose_name=u'实发材料',null=True,blank=True,related_name="auap_actual_storelist")
    actual_quantity=models.IntegerField(verbose_name=u'实发数量',null=True,blank=True)
    status=models.IntegerField(verbose_name=u'领用单状态',choices=AUXILIARY_TOOL_APPLY_CARD_STATUS,default=AUXILIARY_TOOL_APPLY_CARD_APPLICANT)
    applicant=models.ForeignKey(User,verbose_name=u'领料',blank=True,null=True,related_name="at_applicants")
    auditor = models.ForeignKey(User,verbose_name=u"主管",null=True,blank=True,related_name="at_auditor")
    keeper=models.ForeignKey(User,verbose_name=u'发料',blank=True,null=True,related_name="at_keeper")
    remark=models.TextField(verbose_name=u'备注',default="",blank=True,null=True)
"""
