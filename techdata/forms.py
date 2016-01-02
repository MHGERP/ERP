#!/usr/bin/env python
# coding=utf-8
from django import  forms
from const.models import Materiel
from techdata.models import CirculationRoute, CirculationName
from const import PROCESSING_CHOICES

class MaterielForm(forms.ModelForm):
    """
    JunHU
    """
    class Meta:
        model = Materiel
        exclude = ("id", "order")
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
    def clean(self):
        cleaned_data = super(CirculationRouteForm, self).clean()
        for i in range(2, 11):
            curfield = "L%d" % i
            prevfield = "L%d" % (i - 1)
            #print cleaned_data.get(prevfield)
            #print cleaned_data.get(curfield)
            if cleaned_data.get(curfield) != None and cleaned_data.get(prevfield) == None:
                #print "circulation error"
                raise forms.ValidationError("流转路线必须连续")
        return cleaned_data

