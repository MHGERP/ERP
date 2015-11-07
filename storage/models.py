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
