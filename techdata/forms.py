#!/usr/bin/env python
# coding=utf-8
from django import  forms
from const.models import Materiel
from techdata.models import WeldSeam, CirculationRoute
from const import PROCESSING_CHOICES

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
            "material": forms.Select(attrs = {"class": "input-medium"}),
            "count": forms.TextInput(attrs = {"class": "input-medium"}),
            "remark": forms.TextInput(attrs = {"class": "input-medium"}),
        }

    
class ProcessingForm(forms.Form):
    """
    JunHU
    """
    process = forms.ChoiceField(choices = PROCESSING_CHOICES, widget = forms.Select(attrs = {"class": "input-medium"}))

class WeldSeamForm(forms.ModelForm):
    """
    JunHU
    """
    class Meta:
        model = WeldSeam
        exclude = ('materiel_belong',)
        widgets = {
            "weld_index": forms.TextInput(attrs = {"class": "input-small"}),
            "base_metal_thin_1": forms.TextInput(attrs = {"class": "input-small"}),
            "base_metal_thin_2": forms.TextInput(attrs = {"class": "input-small"}),
            "length": forms.TextInput(attrs = {"class": "input-small"}),
            "weight_1": forms.TextInput(attrs = {"class": "input-small"}),
            "weight_2": forms.TextInput(attrs = {"class": "input-small"}),
            "weld_material_1": forms.Select(attrs = {"class": "input-small"}),
            "weld_material_2": forms.Select(attrs = {"class": "input-small"}),
            "weld_method": forms.Select(attrs = {"class": "input-small"}),
            "weldseam_type": forms.Select(attrs = {"class": "input-small"}),
            "size_1": forms.TextInput(attrs = {"class": "input-small"}),
            "size_2": forms.TextInput(attrs = {"class": "input-small"}),
            "remark": forms.TextInput(attrs = {"class": "input-medium"}),
        }
class CirculationRouteForm(forms.ModelForm):
    """
    mxl
    """
    class Meta:
        model = CirculationRoute
        exclude = ('materiel_belong')
        widgets = {
            "L1" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L2" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L3" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L4" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L5" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L6" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L7" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L8" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L9" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L10" : forms.Select(attrs = {"class" : "form-control input-mini"}),
        }
    #def __init__(self, *args, **kwargs):
    #    super(CirculationRouteForm, self).__init__(*args, **kwargs)
    #    for field in self.fields:
    #        self.fields[field] = forms.ChoiceField(widget = forms.Select(attrs = {'class' : 'form-control input-mini',}))

