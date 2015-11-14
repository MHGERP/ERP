from django import  forms
from django.forms import ModelForm
from users.models import *
class userInfoForm(ModelForm):
    class Meta:
        model=UserInfo
        fields=['name','sex','phone','mobile']
        widgets = {
        			'name':forms.TextInput(),
                	'sex':forms.Select(),
                   	'phone':forms.TextInput(),
                   	'mobile':forms.TextInput(),
                   }
        