#!/usr/bin/env python
# coding=utf-8
from const import *
from purchasing.models import MaterielCopy
from models import *

def batchDecentialization(order, inventory_type, DetailItem):
    if inventory_type == OUT_PURCHASED:
       for item in DetailItem.objects.filter(order = order):
            fields = item.materiel_belong._mata.get_all_fields_name()
            materielcopy = MaterielCopy()
            for attr in fields:
                try:
                    if attr != "id":
                        value = getattr(item.materiel_belong, attr)
                        setattr(materielcopy, attr, value)
                except:
                    pass
            
            materielcopy.copy()
