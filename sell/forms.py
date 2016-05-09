#!/usr/bin/env python
# coding=utf-8
from django import forms
from sell.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("id")
        widgets = {
            "mame" : forms.TextInput(attrs = {
                "class" : "input-medium"
            })
        }
