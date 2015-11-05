# coding: UTF-8
from datetime import *
from django import  forms
from django.contrib.admin import widgets

from news import NEWS_MAX_LENGTH
from news.models import NewsCategory

class NewsForm(forms.Form):
    news_title = forms.CharField(max_length=200, required=True,
                                 widget=forms.TextInput(attrs={'class':'span6','id':"news_title",'placeholder':u"新闻标题"}),)
    news_content = forms.CharField(max_length=NEWS_MAX_LENGTH, required=True)
    news_date = forms.DateTimeField(widget=widgets.AdminDateWidget())
    news_cate_list = NewsCategory.objects.all()
    choice_list = []
    for obj in news_cate_list:
        choice_list.append((obj.id, obj.get_category_display()))
    news_category = forms.ChoiceField(choices = choice_list)
    news_document = forms.FileField(label='select', help_text='文件上传', required=False, 
                                    widget=forms.FileInput(attrs={'multiple':'multiple'}))
