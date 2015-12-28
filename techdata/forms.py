#!/usr/bin/env python
# coding=utf-8
from django import  forms
from const.models import Materiel, CirculationRoute, CirculationName

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

