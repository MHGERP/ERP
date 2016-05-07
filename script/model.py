# coding: UTF-8
from django.db import models
from const import *
from django.contrib.auth.models import User
from const.models import *
from purchasing.models import MaterielCopy

one = WorkOrder.objects.get(id = 1)
print one
print "hahahaaaaaaaaaaaaa"
