# coding: UTF-8
from django.db import models
from const import *
from django.contrib.auth.models import User
from const.models import *
from purchasing.models import *
import datetime




# oneObj = Materiel(
#                     order = WorkOrder.objects.get(id = 1),
#                     index = "0982301",
#                     sub_index = "sdfsfd",
#                     schematic_index = "sdsf",
#                     parent_schematic_index = "kfjdsl",
#                     parent_name = "sdklfj",
#                     material = Material.objects.get(id = 1),
#                     name = "sdfsf",
#                     count = "20",
#                     net_weight = "10",
#                     total_weight = "90",
#                     quota = "78",
#                     quota_coefficient = "18",
#                     #inventory_type = "models.ManyToManyField(InventoryType, blank = True, null = True, verbose_name = u"明细表归属")",
#                     remark = "sdfs",
#                     specification = "dsfsfd",
#                     standard = "sdfsdf",
#                     unit = "132124",
#                     status = "sdfsf",
#                     press = "sdfs",
#                     recheck = "lkjs",
#                     detection_level = "dsfk",
#                     complete_plandate = datetime.datetime.now().date(),
#                     complete_date = datetime.datetime.now().date()
#                 )
idtable = {
    MAIN_MATERIEL: "main_materiel",
    AUXILIARY_MATERIEL: "auxiliary_materiel",
    FIRST_FEEDING: "first_feeding",
    OUT_PURCHASED: "purchased",
    COOPERANT: "forging",
    WELD_MATERIAL: "weld_material",
}
# sub=SubWorkOrder.objects.get(pk = 1)
oneObj = MaterielCopy(
                    order = WorkOrder.objects.get(id = 1),
                    index = "0982301",
                    sub_index = "sdfsfd",
                    schematic_index = "sdsf",
                    parent_schematic_index = "kfjdsl",
                    parent_name = "sdklfj",
                    material = Material.objects.get(id = 1),
                    name = "sdfsf",
                    count = "20",
                    net_weight = "10",
                    total_weight = "90",
                    quota = "78",
                    quota_coefficient = "18",
                    #inventory_type = "models.ManyToManyField(InventoryType, blank = True, null = True, verbose_name = u"明细表归属")",
                    remark = "sdfs",
                    specification = "dsfsfd",
                    standard = "sdfsdf",
                    unit = "132124",
                    status = "sdfsf",
                    press = "sdfs",
                    recheck = "lkjs",
                    detection_level = "dsfk",
                    complete_plandate = datetime.datetime.now().date(),
                    complete_date = datetime.datetime.now().date(),
                    relate_material = None,
                    orgin_materiel = Materiel.objects.get(id = 259),
                    work_order = "sdfsfd"
                )

# print oneObj
# print Materiel.objects.all().count()
oneObj.save()
it = InventoryType.objects.get(name = "main_materiel")
# print "===================="
# print it
oneObj.inventory_type.add(InventoryType.objects.get(name = "auxiliary_materiel"))
# twoObj = MaterielPurchasingStatus(
#                     materiel = oneObj,
#                     add_to_detail = True
#                 )
# twoObj.save()
print MaterielCopy.objects.all().count()

# word = MaterielCopy.objects.filter(inventory_type__name=pid, materielpurchasingstatus__add_to_detail = True,relate_material=None)
# for one in word:
#     #print ((one.inventory_type) == "main_materiel")
#     if one.materielpurchasingstatus:
#         print(one.materielpurchasingstatus.add_to_detail)

print "hahahaaaaaaaaaaaaa"
