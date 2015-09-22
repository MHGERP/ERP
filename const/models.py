# coding: UTF-8
from django.db import models
from const import *

class BidFormStatus(models.Model):
    status=models.IntegerField(blank=False,unique=True,choices=BIDFORM_STATUS_CHOICES,verbose_name=u"标单状态")
