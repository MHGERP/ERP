#!/usr/bin/env python
# coding=utf-8

from django import forms
from const import *

class InventoryTypeForm(forms.Form):
    """
    JunHU
    summary: store all type of source inventory list
    """
    inventoryType = forms.ChoiceField(required = True, label = u"明细清单", choices = INVENTORY_TYPE, widget = forms.Select(attrs = {'class': 'input form-control'}))


