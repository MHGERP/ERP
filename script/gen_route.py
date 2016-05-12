#coding= utf-8
import xlrd
from const.models import Materiel
from techdata.models import *
from django.db.models import Q

idtable = {
    "H1": "0",
    "J": "2",
    "R": "3",
    "ZM": "4",
    "GY": "5",
    "DY": "6",
    "XZ": "7",
}
file = "03015007B.xlsx" 
book = xlrd.open_workbook(file)
table = book.sheets()[0]
list = Materiel.objects.filter(order__order_index = "03015007B")

box = []
for rownum in xrange(1, table.nrows):
    route = table.cell(rownum, 10).value
    if not route:
        continue
    processing = []
    for i in xrange(12, 12 + 24 + 1, 2):
        if not table.cell(rownum, i).value:
            break
        processing.append(table.cell(rownum, i).value)
    box.append((route.split(), processing))

for route, item in zip(box, list):
    print item, route[0], route[1]
    for i in xrange(len(route[0])):
        step = CirculationName.objects.get(name = idtable[route[0][i]])
        setattr(item.circulationroute, "L%d" % (i + 1), step)
    item.circulationroute.save()
    for i in xrange(len(route[1])):
        print step
        step = ProcessingName.objects.get(name = route[1][i])
        setattr(item.processing, "GX%d" % (i + 1), step)
    item.processing.save()



