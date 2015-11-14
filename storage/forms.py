# coding: UTF-8
from datetime import *
from django import  forms
from django.forms import ModelForm
from storage.models import *
from const.models import Materiel
from const import ORDERFORM_STATUS_CHOICES, MATERIEL_CHOICE,STORAGEDEPARTMENT_CHOICES
from purchasing.models import PurchasingEntryItems
from django.contrib.auth.models import User
from users.utility import getUserByAuthority
from users import STORAGE_KEEPER
from const.utils import getChoiceList
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

#class WeldingMaterialApplyCardForm(ModelForm):
#    class Meta:
#        model=WeldingMaterialApplyCard
#        exclude=['create_time']

class ApplyCardForm(ModelForm):

    class Meta:
        model=WeldingMaterialApplyCard
        exclude=[]
        
        widgets={
                'workorder':forms.TextInput(attrs={'class':'form-control','style':'width:60%'}),
                'weld_bead_number':forms.TextInput(attrs={'class':'form-control span2'}), 
                'weld_material_number':forms.TextInput(attrs={'class':'form-control '}),
                'model':forms.TextInput(attrs={'class':'form-control'}),
                'standard':forms.TextInput(attrs={'class':'form-control span1'}),
                'apply_weight':forms.TextInput(attrs={'class':'form-control span1'}),
                'apply_quantity':forms.TextInput(attrs={'class':'form-control span1'}),
                'material_number':forms.TextInput(attrs={'class':'form-control '}),
                'actual_weight':forms.TextInput(attrs={'class':'form-control span1'}),
                'actual_quantity':forms.TextInput(attrs={'class':'form-control span1'}),
                #hidden
                'index':forms.HiddenInput(),
                'department':forms.HiddenInput(),
                'create_time':forms.HiddenInput(),
                'applicant':forms.HiddenInput(),
                'auditor':forms.HiddenInput(),
                'inspector':forms.HiddenInput(),
                'commit_user':forms.HiddenInput(),
                'status':forms.HiddenInput(),
                }
class Apply_ApplyCardForm(ApplyCardForm):
    class Meta(ApplyCardForm.Meta):
        widgets={
                'workorder':forms.TextInput(attrs={'class':'form-control','style':'width:60%',}),
                'weld_bead_number':forms.TextInput(attrs={'class':'form-control span2',}), 
                'weld_material_number':forms.TextInput(attrs={'class':'form-control',}),
                'model':forms.TextInput(attrs={'class':'form-control',}),
                'standard':forms.TextInput(attrs={'class':'form-control span1',}),
                'apply_weight':forms.TextInput(attrs={'class':'form-control span1',}),
                'apply_quantity':forms.TextInput(attrs={'class':'form-control span1',}),
                'material_number':forms.TextInput(attrs={'class':'form-control ','readonly':''}),
                'actual_weight':forms.TextInput(attrs={'class':'form-control span1','readonly':''}),
                'actual_quantity':forms.TextInput(attrs={'class':'form-control span1','readonly':''}),
                #hidden
                'index':forms.HiddenInput(),
                'department':forms.HiddenInput(),
                'create_time':forms.HiddenInput(),
                'applicant':forms.HiddenInput(),
                'auditor':forms.HiddenInput(),
                'inspector':forms.HiddenInput(),
                'commit_user':forms.HiddenInput(),
                'status':forms.HiddenInput(),
                }

class Commit_ApplyCardForm(ApplyCardForm):
    class Meta(ApplyCardForm.Meta):
        widgets={
                'workorder':forms.TextInput(attrs={'class':'form-control','style':'width:60%','readonly':''}),
                'weld_bead_number':forms.TextInput(attrs={'class':'form-control span2','readonly':''}), 
                'weld_material_number':forms.TextInput(attrs={'class':'form-control','readonly':''}),
                'model':forms.TextInput(attrs={'class':'form-control','readonly':''}),
                'standard':forms.TextInput(attrs={'class':'form-control span1','readonly':''}),
                'apply_weight':forms.TextInput(attrs={'class':'form-control span1','readonly':''}),
                'apply_quantity':forms.TextInput(attrs={'class':'form-control span1','readonly':''}),
                'material_number':forms.TextInput(attrs={'class':'form-control '}),
                'actual_weight':forms.TextInput(attrs={'class':'form-control span1'}),
                'actual_quantity':forms.TextInput(attrs={'class':'form-control span1'}),
                #hidden
                'index':forms.HiddenInput(),
                'department':forms.HiddenInput(),
                'create_time':forms.HiddenInput(),
                'applicant':forms.HiddenInput(),
                'auditor':forms.HiddenInput(),
                'inspector':forms.HiddenInput(),
                'commit_user':forms.HiddenInput(),
                'status':forms.HiddenInput(),
                }

class EntryItemsForm(ModelForm):
    class Meta:
        model = PurchasingEntryItems
        fields = ("remark","date","price")
        widget = {
            "date":forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd","id":"entryitem_time"})
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
        users = User.objects.all()
        self.fields["purchaser"].choices = getChoiceList(users,"userinfo")


class RefundSearchForm(forms.Form):
    date = forms.DateField(label=u"日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','id':'date'}))
    department = forms.ChoiceField(label=u"退库单位",choices = STORAGEDEPARTMENT_CHOICES,required=False,widget=forms.Select(attrs={"class":'form-control span2','id':'department'}))
    refund_code = forms.CharField(label=u'编号',required=False,widget=forms.TextInput(attrs={'class':'form-control span2','id':'refund_code'}))
    work_order=forms.CharField(label=u'工作令',required=False,widget=forms.TextInput(attrs={'class':'form-control span2','id':'work_order'}))
    keeper=forms.ChoiceField(label=u'库管员',required=False,widget=forms.Select(attrs={'class':'form-control span2','id':'keeper'}))
    def __init__(self,*args,**kwargs):
        super(RefundSearchForm,self).__init__(*args,**kwargs)
        users = getUserByAuthority(STORAGE_KEEPER)
        group = Group.objects.all()
        self.fields["keeper"].choices = getChoiceList(users,"userinfo")
        self.fields["department"].choices = getChoiceList(group,"name")
class WeldRefundForm(ModelForm):
    class Meta:
        model = WeldRefund
        exclude = ('department','date','code','id','refunder','keeper','weldrefund_status')
        widgets = {
            'work_order':forms.Select(attrs={'class':"span2",'readonly':True}),
            'receipts_time':forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd","id":"receipts_time","class":"span2"}),
            'receipts_code': forms.TextInput(attrs={'class':"span2"}),                      
            'type_specification': forms.TextInput(attrs={'class':"span2"}),                      
            'refund_weight': forms.TextInput(attrs={'class':"span1"}),                      
            'refund_count': forms.TextInput(attrs={'class':"span1"}),                      
            'refund_status': forms.TextInput(attrs={'class':"span2"}),                      
        }

class AuxiliaryToolsCardForm(ModelForm):
    class Meta:
        model=AuxiliaryToolApplyCard
        exclude=['create_time','commit_time']

class AuxiliaryToolsForm(ModelForm):
    class Meta:
        model=AuxiliaryTool
        exclude=[]

        widgets={
                'name':forms.TextInput(attrs={'class':'form-control search-query','readonly':'readonly'}),
                'model':forms.TextInput(attrs={'class':'form-control search-query','readonly':'readonly'}),
                'measurement_unit':forms.TextInput(attrs={'class':'form-control search-query','readonly':'readonly'}),
                'unit_price':forms.TextInput(attrs={'class':'form-control search-query','readonly':'readonly'}),
                'manufacturer':forms.TextInput(attrs={'class':'form-control search-query','readonly':'readonly'}),
                'quantity':forms.TextInput(attrs={'class':'form-control search-query'}),
                }

class AuxiliaryToolsSearchForm(forms.Form):
    date=forms.DateField(label=u'日期',required=False,widget=forms.TextInput(attrs={'readonly':'readonly','class':'form-control search-query','id':'date'}))
    name=forms.CharField(label=u'名称',required=False,widget=forms.TextInput(attrs={'class':'form-control search-query','id':'name'}))
    model=forms.CharField(label=u'类别',required=False,widget=forms.TextInput(attrs={'class':'form-control search-query','id':'model'}))
    manufacturer=forms.CharField(label=u'厂家',required=False,widget=forms.TextInput(attrs={'class':'form-control search-query','id':'manufacturer'}))

