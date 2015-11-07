# coding: UTF-8
from datetime import *
from django import  forms
from django.contrib.admin import widgets

from const import NEWS_MAX_LENGTH
from news.models import NewsCategory
from users.models import Group

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

class MessageForm(forms.Form):
    message_title = forms.CharField(max_length=100, required=True,
                                   widget=forms.TextInput(attrs={'class':'span6', 'id':"message_title", 'placeholder':u"消息标题 "}),)
    message_content = forms.CharField(max_length=1000, required=True,
                                      widget=forms.Textarea(attrs={'id':"message_content", 'rows':10, 'cols':80}))
    message_document = forms.FileField(label='select', help_text='文件上传', required=False,
                                    widget=forms.FileInput(attrs={'multiple':'multiple'}))
    message_group_list = Group.objects.all()
    choice_list = []
    for obj in message_group_list:
        choice_list.append((obj.id, obj.name))
    message_groups = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices = choice_list)
