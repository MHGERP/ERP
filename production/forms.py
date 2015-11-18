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
