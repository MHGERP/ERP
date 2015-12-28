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
    class Meta:
        model = CirculationRoute
        exclude = ('materiel_belong')
    def __init__(self, *args, **kwargs):
        super(CirculationRouteForm, self).__init__(*args, **kwargs)
        CIRCULATIONNAME_CHOICES = tuple((item.id, item) for item in CirculationName.objects.all())
        #i = 0
        for field in self.fields:
            print field
            #field = forms.ChoiceField(widget = forms.Select(attrs = {'class' : 'form-control', 'style' : 'width:100px!important'}))
            #field.choices = CIRCULATIONNAME_CHOICES
            #field.label = "L%d" % i
            #i += 1
            self.fields[field] = forms.ChoiceField(widget = forms.Select(attrs = {'class' : 'form-control', 'style' : 'width:100px!important'}))
            self.fields[field].choices = CIRCULATIONNAME_CHOICES
