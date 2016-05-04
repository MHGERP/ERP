from const.models import Materiel
from purchasing.models import MaterielCopy

materiel_set=Materiel.objects.all()
for item in materiel_set:
    print item
    fields=item._meta.get_all_field_names()
    materielcopy=MaterielCopy()
    for attr in fields:
        try:
            value=getattr(item,attr)
            setattr(materielcopy,attr,value)
        except:
            pass
    
    materielcopy.save()

