#!/usr/bin/env python
# coding=utf-8
from const import *
from const.models import SubWorkOrder, InventoryType, Materiel
from purchasing.models import MaterielCopy
from models import *

def batchDecentialization(order, inventory_type, DetailItem):
    """
    JunHU
    """
    for sub_order in SubWorkOrder.objects.filter(order = order):
        if inventory_type == MAIN_MATERIEL:
            for item in DetailItem.objects.filter(order = order):
                materielcopy = MaterielCopy()
                materielcopy.remark = item.remark
                materielcopy.count = item.count
                materielcopy.material = item.material
                materielcopy.net_weight = item.weight
                materielcopy.stardard = item.stardard
                materielcopy.status = item.status
                materielcopy.specification = item.size
                materielcopy.sub_workorder = sub_order
                materielcopy.work_order = item.order

                materielcopy.inventory_type = InventoryType.objects.get(name = inventory_type)
                materielcopy.save()
        else:
            for item in DetailItem.objects.filter(materiel_belong__order = order):
                #materiel = Materiel.objects.get(id = item.materiel_belong.id)
                materiel = item.materiel_belong
                fields = materiel._meta.get_all_field_names()
                materielcopy = MaterielCopy()
                for attr in fields:
                    try:
                        if attr != "id":
                            value = getattr(item.materiel_belong, attr)
                            setattr(materielcopy, attr, value)
                    except:
                        pass
		            
                materielcopy.sub_workorder = sub_order
                materielcopy.remark = item.remark
                materielcopy.work_order = item.materiel_belong.order

                materielcopy.inventory_type = InventoryType.objects.get(name = inventory_type)
                materielcopy.save()

def processDetailGenerate(order):
    """
    JunHU
    """
    for sub_order in SubWorkOrder.objects.filter(order = order):
        SynthesizeFileListStatus(order = sub_order).save()
        for item in Materiel.objects.filter(order = order):

