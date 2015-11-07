# coding: UTF-8
from datetime import *
from django import  forms
from django.forms import ModelForm
from storage.models import *
from const import ORDERFORM_STATUS_CHOICES
from const.models import Materiel
from const import ORDERFORM_STATUS_CHOICES, MATERIEL_CHOICE

DEPARTMENT_CHOICES=(
        (u' ',u'------'),
        (u'部门A',u'部门A'),
        (u'部门B',u'部门B'),
        (u'部门C',u'部门C'),
        (u'部门D',u'部门D'),
        )

class ApplyCardHistorySearchForm(forms.Form):
    date=forms.DateField(label=u'日期',required=False,widget=forms.TextInput(attrs={'readonly':'readonly','class':'form-control search-query','id':'date'}))
    department=forms.ChoiceField(label=u'领用部门',required=False,choices=DEPARTMENT_CHOICES,widget=forms.Select(attrs={'class':'form-control','id':'department'}))
    index=forms.CharField(label=u'编号',required=False,widget=forms.TextInput(attrs={'class':'form-control search-query','id':'index'}))
    work_order=forms.CharField(label=u'工作令',required=False,widget=forms.TextInput(attrs={'class':'form-control search-query','id':'work_order'}))
    commit_user=forms.CharField(label=u'发料人',required=False,widget=forms.TextInput(attrs={'class':'form-control search-query','id':'commit_user'}))

