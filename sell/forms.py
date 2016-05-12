#!/usr/bin/env python
# coding=utf-8
from django import forms
from const import REVIEW_COMMENTS_CHOICES
from sell.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("id", "manufacture_file", "techdata_file", "purchasing_file",)
        widgets = {
            "mame" : forms.TextInput(attrs = {
                "class" : "input-medium"
            })
        }

class BidFileAuditForm(forms.Form):
    status = forms.ChoiceField(choices = REVIEW_COMMENTS_CHOICES, widget = forms.Select(attrs = {"class" : "input-medium"}))
    bid = forms.CharField(widget = forms.TextInput(attrs = {"style" : "display : none"}))
