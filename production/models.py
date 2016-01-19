# coding: UTF-8
from django.db import models
from const.models import WorkOrder


class SynthesizeFileListStatus(models.Model):
    workorder_id = models.ForeignKey(WorkOrder)
    sketch = models.BooleanField(default=False)
    craph = models.BooleanField(default=False)
    product = models.BooleanField(default=False)
    encasement_graph = models.BooleanField(default=False)
    mark = models.BooleanField(default=False)
    encasement_list = models.BooleanField(default=False)
    coating_detail = models.BooleanField(default=False)
    pressure_test = models.BooleanField(default=False)
    class Meta:
        verbose_name = u"综合工部"
        verbose_name_plural = u"综合工部"
    def __unicode__(self):
        return "%s" % self.workorder_id