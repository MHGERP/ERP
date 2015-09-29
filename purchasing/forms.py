# coding: UTF-8
from datetime import *
from django import  forms
from django.forms import ModelForm
from purchasing.models import Supplier
class SupplierForm(ModelForm):
    class Meta:
        model=Supplier
        field=('supplier_id','supplier_name')
        widgets={
            'supplier_id':forms.TextInput(),
            'supplier_name':forms.TextInput(),
        }
