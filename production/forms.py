from django import forms
from django.forms import ModelForm
from const.models import WorkOrder

class OrderIndexForm(forms.Form):
    order_index = forms.ChoiceField(widget = forms.Select(attrs = {'class': 'form-control input-medium'}))
    
    def __init__(self, *args, **kwargs):
        super(OrderIndexForm, self).__init__(*args, **kwargs)
        ORDER_INDEX_CHOICES = tuple((item.order_index,item.order_index) for item in WorkOrder.objects.all())
        self.fields["order_index"].choices = ORDER_INDEX_CHOICES



# coding: UTF-8
from datetime import *
from django import  forms
from const.models import WorkOrder


class TaskAllocationSearchForm(forms.Form):
    workorder_choices=tuple([(-1,"------")]+[(item.id,item.order_index) for item in WorkOrder.objects.all()])
    workorder=forms.ChoiceField(choices=workorder_choices,required=False)
    identifier=forms.CharField(required=False)
    processnumber=forms.CharField(required=False)
    groupnumber=forms.CharField(required=False)

