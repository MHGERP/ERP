#!/usr/bin/env python
# coding=utf-8

from django import forms
from const import *
from const.models import InventoryType, WorkOrder

class WorkOrderForm(forms.Form):
    """
    JunHU
    summary: store all work orders
    """
    work_order = forms.ChoiceField(label=u"工作令", widget = forms.Select(attrs = {"class": "form-control input"}))
    def __init__(self, *args, **kwargs):
        super(WorkOrderForm, self).__init__(*args, **kwargs)
        WORKORDER_CHOICES = tuple((item.id, item) for item in WorkOrder.objects.all())
        self.fields["work_order"].choices = WORKORDER_CHOICES

class AuthorTypeForm(forms.Form):
    """
    JunHU
    summary: store all type of author type
    """
    auth_type = forms.ChoiceField(choices = AUTH_TYPE_CHOICES, widget = forms.Select(attrs = {'class': 'form-control input'}))

class InventoryTypeForm(forms.Form):
    """
    JunHU
    summary: store all type of source inventory list
    """
    TYPE_CHOICES = tuple((item.id, item) for item in InventoryType.objects.all())

    inventory_type = forms.ChoiceField(choices = TYPE_CHOICES, widget = forms.Select(attrs = {'class': 'form-control input'}))


    def __init__(self, *args, **kwargs):
        super(InventoryTypeForm, self).__init__(*args, **kwargs)
        TYPE_CHOICES = tuple((item.id, item) for item in InventoryType.objects.all())
        self.fields["inventory_type"].choices = TYPE_CHOICES





