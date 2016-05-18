# coding: UTF-8
from purchasing.models import StatusChange,ArrivalInspection,MaterielFormConnection
from const.models import BidFormStatus
from const import *
from storage.models import *
from datetime import datetime

def goNextStatus(bidform,user):
    original_status=bidform.bid_status
    new_status=original_status.next_part_status
    change_time=datetime.now()
    status_change=StatusChange(bidform=bidform,original_status=original_status,new_status=new_status,change_user=user,change_time=change_time)
    status_change.save()
    bidform.bid_status=new_status
    bidform.save()


def buildArrivalItems(bidform):
    mat_connection = MaterielFormConnection.objects.filter(order_form = bidform.order_form)
    for mat in mat_connection:
        arrivalIns = ArrivalInspection(bidform = bidform , material = mat.materiel)
        arrivalIns.save()

def goStopStatus(bidform,user):
    original_status=bidform.bid_status
    new_status=BidFormStatus.objects.get(part_status=BIDFORM_STATUS_STOP)
    change_time=datetime.now()
    status_change=StatusChange(bidform=bidform,original_status=original_status,new_status=new_status,change_user=user,change_time=change_time,normal_change=False)
    status_change.save()
    bidform.bid_status=new_status
    bidform.save()

def BidNextStatus(bid_apply):
    bid_apply.status=bid_apply.status.next_status
    bid_apply.save()

def SteelEntryItemAdd(steel_entry,selected):
    for aid in selected:
        arrival_inspection=ArrivalInspection.objects.get(id=aid)
        arrival_inspection.check_pass=True
        arrival_inspection.save()
        item=arrival_inspection.material
        entry_item=SteelMaterialEntryItems(specification=item.specification, 
                                batch_number=item.batch_number,
                               material_mark=item.material.name,
                               material_code=item.quality_number,
                               weight=item.total_weight,
                               unit=item.unit,
                               count=item.count,
                               entry=steel_entry,
                               schematic_index=item.schematic_index,
                               material=item)
        entry_item.save()
        if item.materielcopy_set.count() ==0:
            entry_item.work_order.add(item.sub_workorder)
        else:
            for relate_item in item.materielcopy_set.all():
                entry_item.add(relate_item.sub_workorder)


def OutsideEntryItemAdd(outside_entry,selected):
    for aid in selected:
        arrival_inspection=ArrivalInspection.objects.get(id=aid)
        arrival_inspection.check_pass=True
        arrival_inspection.save()
        item=arrival_inspection.material
        entry_item=OutsideStandardItems(entry=outside_entry,
                                        materiel=item,
                                        schematic_index=item.schematic_index,
                                        specification=item.name,
                                        material_mark=item.material.name,
                                       material_code=item.quality_number,
                                       batch_number=item.batch_number,
                                       unit=item.unit,
                                       count=item.count,
                                       weight=item.net_weight,
                                       remark=item.remark,
                                       ticket_number=item.index,
                                       work_order=item.sub_workorder)
        entry_item.save()


def WeldingEntryItemAdd(wilding_entry,selected):
    for aid in selected:
        arrival_inspection=ArrivalInspection.objects.get(id=aid)
        arrival_inspection.check_pass=True
        arrival_inspection.save()
        item=arrival_inspection.material
        entry_item=WeldMaterialEntryItems(material=item,
                   remark=item.remark,
                    total_weight=item.quota,
                    entry=wilding_entry,
                    material_code=item.quality_number,
                    material_mark=item.material.name,
                    specification=item.specification
                   )
        entry_item.save()

def AuxiliaryEntryItemAdd(auxiliary_entry,selected,accept_supplier):
    for aid in selected:
        arrival_inspection=ArrivalInspection.objects.get(id=aid)
        arrival_inspection.check_pass=True
        arrival_inspection.save()
        item=arrival_inspection.material
        entry_item=AuxiliaryToolEntryItems(name=item.name,
                                           specification=item.specification,
                                           count=item.count,
                                           unit=item.unit,
                                           remark=item.remark,
                                           entry=auxiliary_entry,
                                           supplier=accept_supplier
                                        )
        entry_item.save()

def getEntryCode(code):
    array=[item.entry_code for item in SteelMaterialEntry.objects.filter(entry_code__startswith=code)]
    array=array+[item.entry_code for item in OutsideStandardEntry.objects.filter(entry_code__startswith=code)]
    array=array+[item.entry_code for item in WeldMaterialEntry.objects.filter(entry_code__startswith=code)]
    array=array+[item.entry_code for item in AuxiliaryToolEntry.objects.filter(entry_code__startswith=code)]
    try:
        ret= max(int(item.split("-",1)[1]) for item in array)
        return code+"-"+str(ret+1)
    except:
        return code+"-1"

