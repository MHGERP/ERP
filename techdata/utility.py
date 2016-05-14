#!/usr/bin/env python
# coding=utf-8
from const import *
from const.models import SubWorkOrder, InventoryType, Materiel
from purchasing.models import MaterielCopy
from models import *
from production.models import SynthesizeFileListStatus, SubMateriel, ProcessDetail

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
                        if attr != "id" or attr != "order":
                            value = getattr(item.materiel_belong, attr)
                            setattr(materielcopy, attr, value)
                    except:
                        pass
                materielcopy.sub_workorder = sub_order
                materielcopy.remark = item.remark
                materielcopy.work_order = item.materiel_belong.order
                materielcopy.origin_materiel = materiel
                materielcopy.inventory_type = InventoryType.objects.get(name = inventory_type)
                materielcopy.save()

def processDetailGenerate(order):
    """
    JunHU
    """
    for sub_order in SubWorkOrder.objects.filter(order = order):
        SynthesizeFileListStatus(sub_order = sub_order).save()
        for item in Materiel.objects.filter(order = order):
            if item.index != "1" and item.sub_index == "0": continue
            sub_materiel = SubMateriel(materiel_belong = item, sub_order = sub_order)
            sub_materiel.save()
            for i in xrange(1, 13):
                step = getattr(item.processing, "GX%d" % i)
                if step == None: break
                detail = ProcessDetail()
                detail.sub_materiel_belong = sub_materiel
                detail.processname = step
                detail.process_id = i
                detail.work_hour = 0
                detail.save()

def techdataOrderInitialize(order):
    """
    JunHU
    """
    AuxiliaryMark(order = order).save()
    PrincipalMark(order = order).save()
    CooperantMark(order = order).save()
    FirstFeedingMark(order = order).save()
    OutPurchasedMark(order = order).save()
    WeldQuotaPageMark(order = order).save()
    TransferCardMark(order = order).save()
    ProcessBOMPageMark(order = order).save()
    DesignBOMMark(order = order).save()
    WeldJointTech(order = order).save()
