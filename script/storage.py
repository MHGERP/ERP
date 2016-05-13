#!/usr/bin/env python
# coding=utf-8
from const.models import *

sub_workorders = SubWorkOrder.objects.all()

for item in sub_workorders:
    item.name = item.__unicode__()
    item.save()


