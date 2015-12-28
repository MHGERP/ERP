#!/usr/bin/env python
# coding=utf-8

from django import forms
from django.forms import ModelForm
from const.models import Materiel, Material, CirculationName, CirculationRoute

class MaterielForm(ModelForm):
    class Meta:
        model = Materiel
        fields= ('index', 'schematic_index', 'parent_schematic_index', 'material', 'name', 'count', 'net_weight', 'total_weight', 'remark')
        widgets = {
            'material' : forms.Select(attrs = {"class" : "form-control input"})
        }
    def __init__(self, *args, **kwargs):
        super(MaterielForm, self).__init__(*args, **kwargs)
        MATERIAL_CHOICES = tuple((item.id, item) for item in Material.objects.all())
        self.fields['material'].choices = MATERIAL_CHOICES

class CirculationRouteForm(ModelForm):
    class Meta:
        model = CirculationRoute
        exclude = ('materiel_belong')
    def __init__(self, *args, **kwargs):
        super(CirculationRouteForm, self).__init__(*args, **kwargs)
        CIRCULATIONNAME_CHOICES = tuple((item.id, item) for item in CirculationName.objects.all())
        #i = 0
        for field in self.fields:
            #print field
            #field = forms.ChoiceField(widget = forms.Select(attrs = {'class' : 'form-control', 'style' : 'width:100px!important'}))
            #field.choices = CIRCULATIONNAME_CHOICES
            #field.label = "L%d" % i
            #i += 1
            self.fields[field] = forms.ChoiceField(widget = forms.Select(attrs = {'class' : 'form-control', 'style' : 'width:100px!important'}))
            self.fields[field].choices = CIRCULATIONNAME_CHOICES
