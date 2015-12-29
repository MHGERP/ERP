#coding: utf=8

from django.db import models
from const.models import Materiel
from const import PROCESSING_CHOICES, CIRCULATION_CHOICES

class Processing(models.Model):
    materiel_belong = models.ForeignKey(Materiel, verbose_name = u"所属物料")
    name = models.CharField(blank = False, choices = PROCESSING_CHOICES, max_length = 10, verbose_name = u"工序名")
    next_processing = models.ForeignKey('self', null = True, blank = True, verbose_name = u"下一工序")
    is_first_processing = models.BooleanField(blank = False, default = False, verbose_name = u"首道工序")
    instruction = models.CharField(blank = True, null = True, max_length = 10, verbose_name = u"说明")
    index = models.CharField(blank = True, null = True, max_length = 10, verbose_name = u"工号")
    hour = models.FloatField(blank = True, null = True, verbose_name = u"工时")
    class Meta:
        verbose_name = u"工序"
        verbose_name_plural = u"工序"

    def __unicode__(self):
        return self.materiel_belong.name + "(%s)" % self.get_name_display()

class ProcessReview(models.Model):
    meteriel = models.ForeignKey(Materiel, verbose_name = u"零件")
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

