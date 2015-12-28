#!/usr/bin/env python
# coding=utf-8
from django import  forms
from const.models import Materiel

class MaterielForm(forms.ModelForm):
    """
    JunHU
    """
    class Meta:
        model = Materiel
        exclude = ("id", )
        widgets = {
            "name": forms.TextInput(attrs = {"class": "input-medium"}),
            "index": forms.TextInput(attrs = {"class": "input-small"}),
            "schematic_index": forms.TextInput(attrs = {"class": "input-medium"}),
            "material": forms.TextInput(attrs = {"class": "input-medium"}),
            "count": forms.TextInput(attrs = {"class": "input-medium"}),
            "remark": forms.TextInput(attrs = {"class": "input-medium"}),
        }

    
