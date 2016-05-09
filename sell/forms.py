#!/usr/bin/env python
# coding=utf-8
from django import forms
from sell.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("id", "manufacture_file", "techdata_file", "purchasing_file",)
        widgets = {
            "mame" : forms.TextInput(attrs = {
                "class" : "input-medium"
            })
        }
