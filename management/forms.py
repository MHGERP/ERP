#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-09-11 08:06
# Last modified: 2016-09-11 08:07
# Filename: forms.py
# Description:
# coding: UTF-8
from django import  forms
from django.forms import ModelForm
from users.models import Group
from news.models import NewsCategory
from const import NEW_CATEGORY_CHOICES

class GroupForm(forms.Form):
    """
    JunHU
    summary: store all type of group
    """
    group = forms.ChoiceField(widget = forms.Select(attrs = {'class': 'form-control input'}))

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(GroupForm, self).__init__(*args, **kwargs)
        if request:
            GROUP_CHOICES = tuple((item.id, item) for item in Group.objects.all())
        else:
            GROUP_CHOICES = tuple((item.id, item) for item in Group.objects.all())
        self.fields["group"].choices = GROUP_CHOICES

class NewsCateForm(forms.Form):
	"""
	mxl
	"""
	news_cate = forms.ChoiceField(choices = NEW_CATEGORY_CHOICES ,widget = forms.Select(attrs = {'class' : 'from-control input'}))
