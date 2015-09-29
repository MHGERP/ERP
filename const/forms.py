#!/usr/bin/env python
# coding=utf-8

from django import forms
from const.models import Materiel

class InventoryTypeForm(forms.ModelForm):
    """
    JunHU
    summary: store all type of source inventory list
    """
    class Meta:
        model = Materiel
        include = ("inventory_type", )
        widgets = {
            "inventory_type": forms.Select(attrs = {'class': 'input form-control',})
        }


