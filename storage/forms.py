# coding: UTF-8
from datetime import *
from django import  forms
from django.forms import ModelForm
from storage.models import *
from const.models import Materiel
from const import ORDERFORM_STATUS_CHOICES, MATERIEL_CHOICE,STORAGEDEPARTMENT_CHOICES
from purchasing.models import PurchasingEntryItems
from django.contrib.auth.models import User

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

class EntryItemsForm(ModelForm):
    class Meta:
        model = PurchasingEntryItems
        fields = ("remark","date","price")
        widget = {
            "data":forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd","id":"entryitem_time"})
        }

class HumRecordForm(ModelForm):
    class Meta: 
        model = WeldingMaterialHumitureRecord 
        #fields = ("storeRoom","storeMan","demandTemp","demandHumidity","actualTemperature1","actualHumidity1","actualTemperature2","actualHumidity12","remark")
        widgets = {
            "remark": forms.Textarea(attrs = {"rows":"2","style":"width:600px"}),
       #     "storeRoom":forms.Select(attrs={"class":"form-control"}),
       #     "storeMan":forms.TextInput(attrs={"class":"form-control"}),
       #     "demandTemp":forms.TextInput(attrs={"class":"form-control"}),
        }



class EntrySearchForm(forms.Form):
    date = forms.DateField(label=u"日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','id':'date'}))
    purchaser = forms.ChoiceField(label=u"采购员",required=False,widget=forms.Select(attrs={"class":'form-control span2','id':'purchaser'}))
    work_order=forms.CharField(label=u'工作令',required=False,widget=forms.TextInput(attrs={'class':'form-control span2','id':'work_order'}))
    def __init__(self,*args,**kwargs):
        super(EntrySearchForm,self).__init__(*args,**kwargs)
        Users = User.objects.all()
        purchaser_list = [(-1,u"------")]
        for user in Users:
            purchaser_list.append((user.id,user.username))
        self.fields["purchaser"].choices = tuple(purchaser_list)


class RefundSearchForm(forms.Form):
    date = forms.DateField(label=u"日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','id':'date'}))
    department = forms.ChoiceField(label=u"退库单位",choices = STORAGEDEPARTMENT_CHOICES,required=False,widget=forms.Select(attrs={"class":'form-control span2','id':'department'}))
    refund_code = forms.CharField(label=u'编号',required=False,widget=forms.TextInput(attrs={'class':'form-control span2','id':'refund_code'}))
    work_order=forms.CharField(label=u'工作令',required=False,widget=forms.TextInput(attrs={'class':'form-control span2','id':'work_order'}))
    keeper=forms.ChoiceField(label=u'库管员',required=False,widget=forms.TextInput(attrs={'class':'form-control span2','id':'keeper'}))
    def __init__(self,*args,**kwargs):
        super(RefundSearchForm,self).__init__(*args,**kwargs)
        keeper_list = []
        
        
