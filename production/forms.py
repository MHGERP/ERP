# coding: UTF-8
from datetime import *
from django import  forms
from const import ORDERFORM_STATUS_CHOICES

class OrderFormStatusForm(forms.Form):
    """
    JunHU
    summary: store all step of order form status
    """
    status = forms.ChoiceField(choices = ORDERFORM_STATUS_CHOICES, widget = forms.Select(attrs = {'class': 'form-control input'}))
