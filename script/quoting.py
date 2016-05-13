from purchasing.models import *
from const.models import *
supplier = Supplier.objects.all()
print supplier.count()
inven = InventoryType.objects.all()
print inven[5]
# item = QuotingPrice.objects.all()
# print item.count()
item = QuotingPrice(inventory_type = inven[5], nameorspacification="hoho", material_mark="092183", per_fee="123", unit = "kg", the_supplier=supplier[0])
item.save()
