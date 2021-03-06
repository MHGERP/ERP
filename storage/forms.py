#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-07-26 11:32
# Last modified: 2016-07-26 11:33
# Filename: forms.py
# Description:
# coding: UTF-8
from datetime import *
from django import  forms
from django.forms import ModelForm
from storage.models import *
from const.models import Materiel,SubWorkOrder
from const import ORDERFORM_STATUS_CHOICES, MATERIEL_CHOICE,STORAGEDEPARTMENT_CHOICES,STEEL_TYPE,STEEL,STORAGE_ENTRY_TYPECHOICES,STOREROOM_CHOICES
from django.contrib.auth.models import User
from users.utility import getUserByAuthority
from users import STORAGE_KEEPER
from const.utils import getChoiceList,getDistinctSet

DEPARTMENT_CHOICES=STORAGEDEPARTMENT_CHOICES

def set_form_input_style(dict,style=("style","width:100px;")):
    """
    设定form的样式
    """
    for k , v in dict.items():
        v.widget.attrs[style[0]] = style[1]

def set_form_input_width(dict,width="100px"):
    """
    设定form的样式
    """
    for k , v in dict.items():
        v.widget.attrs["style"] = "width:"+width+";"

class ApplyCardHistorySearchForm(forms.Form):
    create_time__gte = forms.DateField(label=u"起始日期",required=False,widget=forms.TextInput(attrs={"class":'form_control','date_picker':"true"}))
    create_time__lte = forms.DateField(label=u"终止日期",required=False,widget=forms.TextInput(attrs={"class":'form_control','date_picker':"true"}))
    work_order = forms.ChoiceField(label=u"工作令",required = False,widget=forms.Select(attrs={"id":"workorder","class":"form_control","select2":"true"}))
    #weld_bead_number = forms.CharField(label=u"焊缝编号",required=False,widget=forms.TextInput(attrs={"class":"form_control"}))
    material_mark = forms.CharField(label=u"焊材牌号",required=False,widget=forms.TextInput(attrs={"class":"form_control"}))
    model_number = forms.CharField(label=u"型号",required=False,widget=forms.TextInput(attrs={"class":"form_control"}))
    #specification = forms.CharField(label=u"规格",required=False,widget=forms.TextInput(attrs={"class":"form_control"}))
    def __init__(self,*args,**kwargs):
        super(ApplyCardHistorySearchForm,self).__init__(*args,**kwargs)
        workorder_list = SubWorkOrder.objects.all()
        self.fields["work_order"].choices = getChoiceList(workorder_list)
        style = ("style","width:120px;")
        set_form_input_style(self.fields,style)
class ApplyCardForm(ModelForm):

    class Meta:
        model=WeldingMaterialApplyCard
        exclude=['storelist']

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
                'workorder':forms.Select(attrs={'class':'form-control','style':'span2','disabled':'disabled'}),
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
        model = WeldMaterialEntryItems
        fields = ("remark","production_date","price")
        widget = {
            "production_date":forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd",})
        }

class HumRecordForm(ModelForm):
    class Meta:
        model = WeldingMaterialHumitureRecord
        exclude = ("storeMan","id")
        #fields = ("storeRoom","storeMan","demandTemp","demandHumidity","actualTemperature1","actualHumidity1","actualTemperature2","actualHumidity12","remark")
        widgets = {
            "remark": forms.Textarea(attrs = {"rows":"2","style":"width:600px"}),
       #     "storeMan":forms.TextInput(attrs={"class":"form-control"}),
       #     "demandTemp":forms.TextInput(attrs={"class":"form-control"}),
        }

class HumSearchForm(forms.Form):
    date__gte = forms.DateField(label = u"起始日期",required = False, widget = forms.TextInput(attrs={'class':'form-controli span2','date_picker':"true"}))
    date__lte = forms.DateField(label = u"终止日期",required = False, widget = forms.TextInput(attrs={'class':'form-controli span2','date_picker':"true"}))
    def __init__(self,*args,**kwargs):
        super(HumSearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields)
class BakeRecordForm(ModelForm):
    class Meta:
        model = WeldingMaterialBakeRecord
        exclude = ("storeMan",)
        widgets = {
            "remark": forms.Textarea(attrs = {"rows":"2","style":"width:600px"}),
            "date":forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd","id":"date"}),
            "intoheattime":forms.DateTimeInput(attrs={"data-date-format":"yyyy-mm-dd hh:ii","id":"intoheattime"}),
            "timefortemp":forms.DateTimeInput(attrs={"data-date-format":"yyyy-mm-dd hh:ii","id":"timefortemp"}),
            "tempfalltime":forms.DateTimeInput(attrs={"data-date-format":"yyyy-mm-dd hh:ii","id":"tempfalltime"}),
            "timeforremainheat":forms.DateTimeInput(attrs={"data-date-format":"yyyy-mm-dd hh:ii","id":"timeforremainheat"}),
            "usetime":forms.DateTimeInput(attrs={"data-date-format":"yyyy-mm-dd hh:ii","id":"usetime"}),
        }
    def __init__(self,*args,**kwargs):
        super(BakeRecordForm,self).__init__(*args,**kwargs)
        engineers = getUserByAuthority(STORAGE_KEEPER)
        engin_tuple = tuple([ (user.id,user.userinfo) for user in engineers ])
        self.fields["weldengineer"].choices = engin_tuple

class BakeSearchForm(forms.Form):
    date__gte = forms.DateField(label = u"起始日期",required = False, widget = forms.TextInput(attrs={'class':'form-controli span2','date_picker':"true"}))
    date__lte = forms.DateField(label = u"终止日期",required = False, widget = forms.TextInput(attrs={'class':'form-controli span2','date_picker':"true"}))
    standardnum = forms.CharField(label = u"标准号",required = False, widget = forms.TextInput(attrs={"class":'form-control span2','id':'standardnum'}))
    def __init__(self,*args,**kwargs):
        super(BakeSearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields)
class ApplyRefundSearchForm(forms.Form):
    id = forms.ChoiceField(label = u"工作令",required = False, widget = forms.Select(attrs={"class":'form-control span2','select2':'true'}))
    order__product_name__contains = forms.CharField(label = u"产品名称",required = False, widget = forms.TextInput(attrs={"class":'form-control span2','id':'product_name'}))
    def __init__(self,*args,**kwargs):
        super(ApplyRefundSearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields,"130px")
        workorder_list = SubWorkOrder.objects.all()
        self.fields["id"].choices = getChoiceList(workorder_list)
class EntrySearchForm(forms.Form):
    entry_time = forms.DateField(label=u"日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','id':'entry_time'}))
    purchaser = forms.ChoiceField(label=u"采购员",required=False,widget=forms.Select(attrs={"class":'form-control span2','id':'purchaser'}))
    entry_code=forms.CharField(label=u'入库单编号',required=False,widget=forms.TextInput(attrs={'class':'form-control span2','id':'entry_code'}))
    def __init__(self,*args,**kwargs):
        super(EntrySearchForm,self).__init__(*args,**kwargs)
        users = getUserByAuthority(STORAGE_KEEPER)
        self.fields["purchaser"].choices = getChoiceList(users,"userinfo")



class SteelEntrySearchForm(forms.Form):
    create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control',"date_picker":'true'}))
    create_time__lte = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control',"date_picker":'true'}))
    entry_code = forms.CharField(label=u'入库单编号',required=False,widget=forms.TextInput(attrs={'class':'form-control span2','id':'form_code'}))
    material_source = forms.CharField(label=u'货物来源',required=False,widget=forms.TextInput(attrs={'class':'form-control span2','id':'material_source'}))
    def __init__(self,*args,**kwargs):
        super(SteelEntrySearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields)

class steelEntryItemsForm(forms.Form):
    store_room = forms.ChoiceField(widget = forms.Select(attrs = {'class': 'form-control input-medium span3'}),label = u"库房位置")
    def __init__(self, *args, **kwargs):
        super(steelEntryItemsForm, self).__init__(*args, **kwargs)
        STORE_ROOM_CHOICES = tuple([(item.id,item.name) for item in StoreRoom.objects.all()])
        self.fields["store_room"].choices = STORE_ROOM_CHOICES

class steelEntryRemarkForm(ModelForm):
    class Meta:
        model = SteelMaterialEntry
        fields = ("remark",)

class RefundSearchForm(forms.Form):
    apply_card__workorder=forms.ChoiceField(label=u'工作令',required=False,widget=forms.Select(attrs={'class':'form-control span2','id':'work_order',"select2":"true"}))
    apply_card__weld_bead_number=forms.CharField(label=u'焊缝编号',required=False,widget=forms.TextInput(attrs={'class':'form-control span2','id':'work_order'}))
    create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control','date_picker':'true',}))
    create_time__lte = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control','date_picker':'true',}))
    def __init__(self,*args,**kwargs):
        super(RefundSearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields,"120px")
        workorder_list = SubWorkOrder.objects.all()
        self.fields["apply_card__workorder"].choices = getChoiceList(workorder_list)
class WeldRefundForm(ModelForm):
    class Meta:
        model = WeldRefund
        exclude = ('department','date','code','id','refunder','keeper','weldrefund_status',)
        widgets = {
            'work_order':forms.HiddenInput(),
            'receipts_time':forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd","id":"receipts_time","class":"span2","disabled":True}),
            'receipts_code': forms.Select(attrs={'class':"span2","disabled":True}),
            'specification': forms.TextInput(attrs={'class':"span2","readonly":True}),
            'refund_weight': forms.TextInput(attrs={'class':"span1","readonly":True}),
            'refund_count': forms.TextInput(attrs={'class':"span1","readonly":True}),
            'refund_status': forms.TextInput(attrs={'class':"span2"}),
        }


class AuxiliaryToolsCardCommitForm(ModelForm):
    class Meta:
        model=AuxiliaryToolApplyCard
        exclude=['create_time','commit_time']

        widgets={
                'remark':forms.HiddenInput(),
                'apply_quantity':forms.HiddenInput(),
                'apply_item':forms.HiddenInput(),
                'actual_quantity':forms.TextInput(attrs={'class':'form-control search-query'}),
                'index':forms.HiddenInput(),
                'apply_total':forms.HiddenInput(),
                'actual_total':forms.HiddenInput(),
                'status':forms.HiddenInput(),
                'applicant':forms.HiddenInput(),
                }
class AuxiliaryToolsCardApplyForm(ModelForm):
    class Meta:
        model=AuxiliaryToolApplyCard
        exclude=['create_time','commit_time']

        widgets={
                'remark':forms.TextInput(attrs={'class':'form-control search-query','style':'width:90%'}),
                'apply_quantity':forms.TextInput(attrs={'class':'form-control search-query'}),
                'actual_quantity':forms.HiddenInput(),
                'index':forms.HiddenInput(),
                'apply_total':forms.HiddenInput(),
                'actual_total':forms.HiddenInput(),
                'status':forms.HiddenInput(),
                }

class AuxiliaryToolsForm(ModelForm):
    class Meta:
        model=AuxiliaryToolStoreList
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
    model=forms.ChoiceField(label=u'类别',choices=AUXILIARY_TOOLS_MODELS_CHOICES,required=False,widget=forms.Select(attrs={'class':'form-control search-query','id':'model'}))
    manufacturer=forms.CharField(label=u'厂家',required=False,widget=forms.TextInput(attrs={'class':'form-control search-query','id':'manufacturer'}))

class AuxiliaryToolsApplyCardSearchForm(forms.Form):
    create_time__gte=forms.DateField(label=u'起始日期',required=False,widget=forms.TextInput(attrs={'class':'form-control','date_picker':'true'}))
    create_time__lte=forms.DateField(label=u'终止日期',required=False,widget=forms.TextInput(attrs={'class':'form-control','date_picker':'true'}))
    apply_storelist__entry_item__name =forms.CharField(label=u'申请物资',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    department=forms.CharField(label=u'领用单位',required=False,widget=forms.TextInput(attrs={'class':'form-control',}))
    applycard_code=forms.CharField(label=u'编号',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))


class AuxiliaryEntrySearchForm(forms.Form):
    create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control','date_picker':'true'}))
    create_time__lte  = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control', 'date_picker':'true'}))
    entry_code=forms.CharField(label=u'入库单编号',required=False,widget=forms.TextInput(attrs={'class':'form-control date_picker','id':'entry_code'}))


    def __init__(self, *args, **kwargs):
        super(AuxiliaryEntrySearchForm, self).__init__(*args, **kwargs)
        set_form_input_width(self.fields,"120px")

class SteelApplyCardSearchForm(forms.Form):
    create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','date_picker':'true','id':'date'}))
    create_time__lte = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','date_picker':'true','id':'date'}))
    applycard_code = forms.CharField(label=u'编号',required=False,widget=forms.TextInput(attrs={'class':'form-control span2','id':'form_code'}))



class AccountSearchForm(forms.Form):
    entry_item__entry__create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','date_picker':'true',}))
    entry_item__entry__create_time__lte = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','date_picker':'true',}))

class AccountWeldApplySearchForm(forms.Form):
    create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','date_picker':'true',}))
    create_time__lte = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','date_picker':'true',}))

class AccountApplySearchForm(forms.Form):
    apply_card__create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','date_picker':'true',}))
    apply_card__create_time__lte = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','date_picker':'true',}))

class AccountEntrySearchForm(forms.Form):
    entry__create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','date_picker':'true',}))
    entry__create_time__lte = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','date_picker':'true',}))

class WeldStorageSearchForm(AccountSearchForm):
    entry_item__material_mark=forms.CharField(label=u'牌号',required=False,widget=forms.TextInput(attrs={'class':'form-control','id':'brand'}))
    entry_item__specification=forms.CharField(label=u'规格',required=False,widget=forms.TextInput(attrs={'class':'form-control','id':'specification'}))
    def __init__(self,*args,**kwargs):
        super(WeldStorageSearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields)

class WeldEntryAccountSearchForm(AccountEntrySearchForm):
    material_mark=forms.CharField(label=u'牌号',required=False,widget=forms.TextInput(attrs={'class':'form-control',}))
    specification=forms.CharField(label=u'规格',required=False,widget=forms.TextInput(attrs={'class':'form-control',}))
    def __init__(self,*args,**kwargs):
        super(WeldEntryAccountSearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields)

class WeldApplyAccountSearchForm(AccountWeldApplySearchForm):
    work_order = forms.ChoiceField(label=u"工作令",required = False,widget=forms.Select(attrs={"class":'form-control','id':'workorder','select2':'true'}))
    weld_bead_number = forms.CharField(label=u"焊缝编号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    applycard_code = forms.CharField(label=u"编号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    def __init__(self,*args,**kwargs):
        super(WeldApplyAccountSearchForm,self).__init__(*args,**kwargs)
        work_order_set = SubWorkOrder.objects.all()
        self.fields["work_order"].choices = getChoiceList(work_order_set,"name")
        set_form_input_width(self.fields,"130px")


class SteelEntryAccountSearchForm(AccountEntrySearchForm):
    work_order = forms.ChoiceField(label=u"工作令",required = False,widget=forms.Select(attrs={"class":'form-control','id':'workorder','select2':'true'}))
    material_mark = forms.CharField(label=u"材料牌号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    specification =  forms.CharField(label=u"规格",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    material_code = forms.CharField(label=u"标记号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    def __init__(self,*args,**kwargs):
        super(SteelEntryAccountSearchForm,self).__init__(*args,**kwargs)
        work_order_set = SubWorkOrder.objects.all()
        self.fields["work_order"].choices = getChoiceList(work_order_set,"name")
        set_form_input_width(self.fields,"100px")
        self.fields["work_order"].widget.attrs["style"] = "width:130px;"

class SteelApplyAccountSearchForm(AccountApplySearchForm):
    work_order = forms.ChoiceField(label=u"工作令",required = False,widget=forms.Select(attrs={"class":'form-control','id':'workorder','select2':'true'}))
    material_mark = forms.CharField(label=u"材料牌号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    specification =  forms.CharField(label=u"规格",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    material_code = forms.CharField(label=u"材质编号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    def __init__(self,*args,**kwargs):
        super(SteelApplyAccountSearchForm,self).__init__(*args,**kwargs)
        work_order_set = SubWorkOrder.objects.all()
        self.fields["work_order"].choices = getChoiceList(work_order_set,"name")
        set_form_input_width(self.fields,"100px")
        self.fields["work_order"].widget.attrs["style"] = "width:130px;"
class SteelStorageAccountSearchForm(AccountSearchForm):
    entry_item__work_order = forms.ChoiceField(label=u"工作令",required = False,widget=forms.Select(attrs={"class":'form-control','id':'workorder','select2':'true'}))
    entry_item__material_mark = forms.CharField(label=u"材料牌号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    specification =  forms.CharField(label=u"规格",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    entry_item__material_code = forms.CharField(label=u"标记号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    def __init__(self,*args,**kwargs):
        super(SteelStorageAccountSearchForm,self).__init__(*args,**kwargs)
        work_order_set = SubWorkOrder.objects.all()
        self.fields["entry_item__work_order"].choices = getChoiceList(work_order_set,"name")
        set_form_input_width(self.fields,"100px")
        self.fields["entry_item__work_order"].widget.attrs["style"] ="width:130px;"

class OutsideEntryAccountSearchForm(AccountEntrySearchForm):
    work_order = forms.ChoiceField(label=u"工作令",required = False,widget=forms.Select(attrs={"class":'form-control','id':'workorder','select2':'true'}))
    schematic_index = forms.CharField(label=u"标准号/图号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    specification =  forms.CharField(label=u"规格",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    material_code = forms.CharField(label=u"标记号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    def __init__(self,*args,**kwargs):
        super(OutsideEntryAccountSearchForm,self).__init__(*args,**kwargs)
        work_order_set = SubWorkOrder.objects.all()
        self.fields["work_order"].choices = getChoiceList(work_order_set,"name")
        set_form_input_width(self.fields,"100px")
        self.fields["work_order"].widget.attrs["style"] ="width:130px;"

class OutsideApplyAccountSearchForm(AccountApplySearchForm):
    work_order = forms.ChoiceField(label=u"工作令",required = False,widget=forms.Select(attrs={"class":'form-control','id':'workorder','select2':'true'}))
    schematic_index = forms.CharField(label=u"标准号/图号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    specification =  forms.CharField(label=u"规格",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    material_code = forms.CharField(label=u"标记号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    def __init__(self,*args,**kwargs):
        super(OutsideApplyAccountSearchForm,self).__init__(*args,**kwargs)
        work_order_set = SubWorkOrder.objects.all()
        self.fields["work_order"].choices = getChoiceList(work_order_set,"name")
        set_form_input_width(self.fields,"100px")
        self.fields["work_order"].widget.attrs["style"] ="width:130px;"

class OutsideStorageAccountSearchForm(AccountSearchForm):
    entry_item__work_order = forms.ChoiceField(label=u"工作令",required = False,widget=forms.Select(attrs={"class":'form-control','id':'workorder','select2':'true'}))
    entry_item__schematic_index =  forms.CharField(label=u"标准号/图号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    entry_item__specification =  forms.CharField(label=u"规格",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    entry_item__material_code = forms.CharField(label=u"标记号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    def __init__(self,*args,**kwargs):
        super(OutsideStorageAccountSearchForm,self).__init__(*args,**kwargs)
        work_order_set = SubWorkOrder.objects.all()
        self.fields["entry_item__work_order"].choices = getChoiceList(work_order_set,"name")
        set_form_input_width(self.fields,"100px")
        self.fields["entry_item__work_order"].widget.attrs["style"] ="width:130px;"


class AuxiliaryToolStorageAccountSearchForm(AccountSearchForm):
    entry_item__material_mark=forms.CharField(label=u'牌号',required=False,widget=forms.TextInput(attrs={'class':'form-control','id':'brand'}))
    entry_item__specification=forms.CharField(label=u'规格',required=False,widget=forms.TextInput(attrs={'class':'form-control','id':'specification'}))
    entry_item__factory=forms.CharField(label=u'厂家',required=False,widget=forms.TextInput(attrs={'class':'form-control',}))
    entry_item__supplier=forms.CharField(label=u'供货商',required=False,widget=forms.TextInput(attrs={'class':'form-control',}))
    def __init__(self,*args,**kwargs):
        super(AuxiliaryToolStorageAccountSearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields)

class AuxiliaryToolEntryAccountSearchForm(AccountEntrySearchForm):
    name=forms.CharField(label=u'名称',required=False,widget=forms.TextInput(attrs={'class':'form-control',}))
    specification=forms.CharField(label=u'规格',required=False,widget=forms.TextInput(attrs={'class':'form-control',}))
    factory=forms.CharField(label=u'厂家',required=False,widget=forms.TextInput(attrs={'class':'form-control',}))
    supplier=forms.CharField(label=u'供货商',required=False,widget=forms.TextInput(attrs={'class':'form-control',}))
    def __init__(self,*args,**kwargs):
        super(AuxiliaryToolEntryAccountSearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields)

class AuxiliaryToolApplyAccountSearchForm(AccountWeldApplySearchForm):
    department = forms.CharField(label=u"领用单位",required = False,widget=forms.TextInput(attrs={"class":'form-control',}))
    actual_storelist__entry_item__name = forms.CharField(label=u"材料名称",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    applycard_code = forms.CharField(label=u"料单编号",required = False,widget=forms.TextInput(attrs={"class":'form-control'}))
    def __init__(self,*args,**kwargs):
        super(AuxiliaryToolApplyAccountSearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields,"100px")


class EntryTypeForm(forms.Form):
    entry_type=forms.ChoiceField(label=u'入库单类型',choices=STORAGE_ENTRY_TYPECHOICES,required=True,widget=forms.Select(attrs={'class':'form-control span2','id':'work_order'}))

class OutsideEntrySearchForm(EntrySearchForm):
    def __init__(self,*args,**kwargs):
        super(OutsideEntrySearchForm,self).__init__(*args,**kwargs)

class StorageEntryAForm(forms.Form):
    change_code = forms.CharField(label=u"修改号",required=False,widget=forms.TextInput())
    sample_report = forms.CharField(label=u"样表",required=False,widget=forms.TextInput())
    entry_code = forms.CharField(label=u"单据编号",required=False,widget=forms.TextInput())
    source = forms.CharField(label=u"货物来源",required=False,widget=forms.TextInput())
    change_code = forms.CharField(label=u"检查记录表编号",required=False,widget=forms.TextInput())
    change_code = forms.CharField(label=u"订购单编号",required=False,widget=forms.TextInput())
    remark = forms.CharField(label=u"备注",required=False,widget=forms.Textarea(attrs={"cols":80,"rows":4,"style":"max-height:50px;overflow:auto"}))

class StorageOutsideEntryInfoForm(ModelForm):
    class Meta:
        model = OutsideStandardEntry
        exclude = ("id","entry_status","purchaser","inspector","keeper","remark","bidform")
    def __init__(self,*args,**kwargs):
        super(StorageOutsideEntryInfoForm,self).__init__(*args,**kwargs)
        for k,v in self.fields.items():
            v.widget.attrs["readonly"] = True
        self.fields["entry_code"].widget.attrs.pop("readonly")

class StorageOutsideEntryRemarkForm(ModelForm):
    class Meta:
        model = OutsideStandardEntry
        fields = ("remark",)
        widgets = {
            "remark":forms.Textarea(attrs={"rows":"10","cols":"40","style":"max-height:80px;overflow-y:auto"}),
        }
class ThreadEntryItemsForm(ModelForm):
    class Meta:
        model = WeldStoreThread
        fields = ("specification","count",)
        widget = {
            "specification": forms.TextInput(attrs={'class':"form-control span1"}),
            "count": forms.TextInput(attrs={'class':"form_control span2"}),
        }

class ThreadSearchForm(ModelForm):
        class Meta:
            model = WeldStoreThread
            fields = ("specification",)
            widget = {
                "specification": forms.TextInput(attrs={'class':"form-control span1"}),
            }
class OutsideApplyCardSearchForm(forms.Form):
    date = forms.DateField(label=u"日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','id':'date'}))
    workorder = forms.ChoiceField(label=u"工作令",required=False,widget=forms.Select(attrs={"class":'form-control span2','id':'workorder'}))
    proposer=forms.ChoiceField(label=u"领用人",required=False,widget=forms.Select(attrs={'class':'form-control span2','id':'proposer'}))
    entry_code = forms.CharField(label=u"领用单号",required=False,widget=forms.TextInput(attrs={"class":'form-control span2','id':'entry_code'}))
    def __init__(self,*args,**kwargs):
        super(OutsideApplyCardSearchForm,self).__init__(*args,**kwargs)

class OutsideApplyCardForm(ModelForm):
    class Meta:
        model = OutsideStandardEntry

class OutsideStorageSearchForm(forms.Form):
    texture = forms.CharField(label=u'材质',required=False,widget=forms.TextInput(attrs={'class':'form-control search-in','id':'texture'}))
    specification=forms.CharField(label=u'规格',required=False,widget=forms.TextInput(attrs={'class':'form-control search-in','id':'specification'}))
class OutsideAccountEntrySearchForm(forms.Form):
    date = forms.DateField(label=u"日期",required = False, widget=forms.TextInput(attrs={'id':'date','class':"span2"}))
    specification = forms.CharField(label=u"规格",required = False,widget=forms.TextInput(attrs={'id':'specification','class':"span2"}))
    entry_code = forms.CharField(label=u"入库单编号",required = False, widget=forms.TextInput(attrs={'id':'entry_code','class':"span2"}))
    work_order = forms.ChoiceField(label=u"工作令",required = False, widget=forms.Select(attrs={'id':'work_order','class':"span2",'select2':'true'}))
    def __init__(self,*args,**kwargs):
        super(OutsideAccountEntrySearchForm,self).__init__(*args,**kwargs)
        workorders = getDistinctSet(SubWorkOrder,WorkOrder,'id')
        self.fields['work_order'].choices = getChoiceList(workorders,'order_index')

class OutsideAccountApplyCardSearchForm(forms.Form):
    date = forms.DateField(label=u"日期",required = False, widget=forms.TextInput(attrs={'id':'date'}))
    specification = forms.CharField(label=u"规格",required = False,widget=forms.TextInput(attrs={'id':'specification'}))
    department = forms.CharField(label=u"领用单位",required = False,widget=forms.TextInput(attrs={'id':'department'}))
    entry_code = forms.CharField(label=u"领用单编号",required = False, widget=forms.TextInput(attrs={'id':'entry_code'}))
    work_order = forms.ChoiceField(label=u"工作令",required = False, widget=forms.Select(attrs={'id':'work_order','select2':'true'}))
    def __init__(self,*args,**kwargs):
        super(OutsideAccountApplyCardSearchForm,self).__init__(*args,**kwargs)
        for key,val in self.fields.items():
            val.widget.attrs["style"] = 'width:120px;'
        self.fields["work_order"].choices = getChoiceList(getDistinctSet(OutsideApplyCard,SubWorkOrder,'workorder',entry_status=STORAGESTATUS_END),'order_index')


class StoreRoomForm(ModelForm):
    class Meta:
        model = StoreRoom
        widget = {
            "material_type": forms.Select(attrs = {"class":'form-control'}),
            "name": forms.TextInput(attrs = {"style":"width:220px"}),
            "position": forms.TextInput(attrs = {"style":"width:220px"}),
        }

    def __init__(self,*args,**kwargs):
        super(StoreRoomForm, self).__init__(*args, **kwargs)
        self.fields["material_type"].choices = STOREROOM_CHOICES


class StoreRoomSearchForm(forms.Form):
    name = forms.CharField(label=u"库房名称",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    position = forms.CharField(label=u"位置",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    material_type = forms.ChoiceField(label=u"材料类型",required = False, widget = forms.Select(attrs={"class":'form-control'}))

    def __init__(self,*args,**kwargs):
        super(StoreRoomSearchForm, self).__init__(*args, **kwargs)
        type_list = [(-1, u"---------"),]
        type_list.extend(list(STOREROOM_CHOICES))

        self.fields["material_type"].choices = tuple(type_list)

class CheckMaterielDbForm(forms.Form):
    db_type = forms.ChoiceField(label=u"材料类型",required = True,choices = MATERIEL_TYPE_CHOICES,widget = forms.Select(attrs={'class':"span2","id":"db_type"}))

class CheckMaterielListForm(forms.Form):
    materiel_type = forms.ChoiceField(label=u"库存材料",required = False, widget=forms.Select(attrs={'id':'materiel_type','class':"span2",'select2':'true'}))
    def __init__(self,*args,**kwargs):
        super(CheckMaterielListForm,self).__init__(*args,**kwargs)

class WeldEntrySearchForm(forms.Form):
    create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control date_picker','date_picker':'true'}))
    create_time__lte  = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control date_picker', 'date_picker':'true'}))
    entry_code=forms.CharField(label=u'入库单编号',required=False,widget=forms.TextInput(attrs={'class':'form-control date_picker','id':'entry_code'}))



class WeldRefundConfirmForm(ModelForm):
    class Meta:
        model = WeldRefund
        fields = ("refund_weight","refund_status")

class SteelMaterialSearchForm(forms.Form):
    entry_item__work_order = forms.ChoiceField(label=u"工作令",required = False, widget = forms.Select(attrs={"class":'form-control'}))
    specification = forms.CharField(label=u"规格",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    entry_item__material_mark = forms.CharField(label=u"材质",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    def __init__(self,*args,**kwargs):
        super(SteelMaterialSearchForm,self).__init__(*args,**kwargs) 
        work_order_set = SubWorkOrder.objects.all()
        self.fields["entry_item__work_order"].choices = getChoiceList(work_order_set,"name")
        set_form_input_width(self.fields,"100px")
        self.fields["entry_item__work_order"].widget.attrs["style"] ="width:130px"

class SteelRefundSearchForm(forms.Form):
    create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control date_picker','date_picker':'true'}))
    create_time__lte  = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control date_picker', 'date_picker':'true'}))
    work_order = forms.ChoiceField(label=u"工作令",required = False,widget=forms.Select(attrs={"class":'form-control',"select2":'true'}))
    refund_code = forms.CharField(label=u'退库单编号',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    def __init__(self,*args,**kwargs):
        super(SteelRefundSearchForm,self).__init__(*args,**kwargs)
        workorder_list = SubWorkOrder.objects.all()
        self.fields["work_order"].choices = getChoiceList(workorder_list,"name")
        set_form_input_width(self.fields,"130px")

class OutsideEntrySearchForm(forms.Form):
    create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control date_picker','date_picker':'true'}))
    create_time__lte  = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control date_picker', 'date_picker':'true'}))
    entry_code = forms.CharField(label=u'入库单编号',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    material_source =  forms.CharField(label=u'货物来源',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    outsidebuy_type = forms.ChoiceField(label=u"材料类型",required=False,widget=forms.Select(attrs={'class':'form-control'}))
    
    def __init__(self,*args,**kwargs):
        super(OutsideEntrySearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields)
        outsidetypes = [("-1","------")]
        outsidetypes.extend(OUTSIDEBUY_TYPE)
        self.fields["outsidebuy_type"].choices = tuple(outsidetypes)

class OutsideEntryItemForm(ModelForm):
    class Meta:
        model = OutsideStandardItems
        fields = ("weight","heatnum","factory","ticket_number","remark")
        widgets =  {
            "weight":forms.TextInput(attrs={"class":"span2"}),
            "heatnum":forms.TextInput(attrs={"class":"span2"}),
            "factory":forms.TextInput(attrs={"class":"span2"}),
            "ticket_number":forms.TextInput(attrs={"class":"span2"}),
            "remark":forms.TextInput(attrs={"class":"span2"}),
        }
    def __init__(self,*args,**kwargs):
        super(OutsideEntryItemForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields,"250px")

class OutsideApplyCardSearchForm(forms.Form):
    create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control date_picker','date_picker':'true'}))
    create_time__lte  = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control date_picker', 'date_picker':'true'}))
    work_order = forms.ChoiceField(label=u"工作令",required=False,widget=forms.Select(attrs={'class':'form-control',"select2":'true'}))
    applycard_code = forms.CharField(label=u'领用卡编号',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    department = forms.CharField(label=u'领用单位',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    def __init__(self,*args,**kwargs):
        super(OutsideApplyCardSearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields)
        workorder_set = SubWorkOrder.objects.all()
        self.fields["work_order"].choices = getChoiceList(workorder_set)
        self.fields["work_order"].widget.attrs["style"] = "width:150px;"

class OutsideMaterialSearchForm(forms.Form):
    entry_item__work_order = forms.ChoiceField(label=u"工作令",required = False, widget = forms.Select(attrs={"class":'form-control'}))
    outsidebuy_type = forms.ChoiceField(label=u"材料类型",required = False, widget = forms.Select(attrs={"class":'form-control'}))
    entry_item__material_mark = forms.CharField(label=u"材质",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    entry_item__schematic_index = forms.CharField(label=u"零件图/标准",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    entry_item__specification = forms.CharField(label=u"名称规格",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    def __init__(self,*args,**kwargs):
        super(OutsideMaterialSearchForm,self).__init__(*args,**kwargs) 
        set_form_input_width(self.fields)
        outsidetypes = [("-1","------")]
        outsidetypes.extend(OUTSIDEBUY_TYPE)
        self.fields["outsidebuy_type"].choices = tuple(outsidetypes)
        work_order_set = SubWorkOrder.objects.all()
        self.fields["entry_item__work_order"].choices = getChoiceList(work_order_set,"name")
        set_form_input_width(self.fields,"100px")
        self.fields["entry_item__work_order"].widget.attrs["style"] ="width:130px"

class WeldMaterialSearchForm(forms.Form):
    entry_item__material__name = forms.CharField(label=u"名称",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    entry_item__material_mark = forms.CharField(label=u"牌号",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    entry_item__model_number = forms.CharField(label=u"型号",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    entry_item__specification = forms.CharField(label=u"规格",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    entry_item__material_code = forms.CharField(label=u"材质编号",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    def __init__(self,*args,**kwargs):
        super(WeldMaterialSearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields)

class OutsideRefundSearchForm(forms.Form):
    create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control date_picker','date_picker':'true'}))
    create_time__lte  = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control date_picker', 'date_picker':'true'}))
    work_order = forms.ChoiceField(label=u"工作令",required=False,widget=forms.Select(attrs={'class':'form-control',"select2":'true'}))
    refund_code = forms.CharField(label=u'退库单编号',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    apply_card__department = forms.CharField(label=u'领用单位',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    def __init__(self,*args,**kwargs):
        super(OutsideRefundSearchForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields)
        workorder_set = SubWorkOrder.objects.all()
        self.fields["work_order"].choices = getChoiceList(workorder_set)
        self.fields["work_order"].widget.attrs["style"] = "width:150px;"

class AuxiliaryToolMaterialSearchForm(forms.Form):
    entry_item__name = forms.CharField(label=u"名称",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    entry_item__specification = forms.CharField(label=u"规格",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    entry_item__factory = forms.CharField(label=u"厂家",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    entry_item__supplier = forms.CharField(label=u"供货商",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    def __init__(self,*args,**kwargs):
        super(AuxiliaryToolMaterialSearchForm,self).__init__(*args,**kwargs) 
        set_form_input_width(self.fields)

class AuxiliaryToolsApplyItemForm(ModelForm):
    class Meta:
        model = AuxiliaryToolApplyCard
        fields = ("actual_count",)
        widgets =  {
            "actual_count":forms.TextInput(attrs={"class":"span2","style":"width:150px;"}),
        }
    def __init__(self,*args,**kwargs):
        super(AuxiliaryToolsApplyItemForm,self).__init__(*args,**kwargs)
        self.fields["actual_count"].required = True

class WeldAccountItemForm(ModelForm):
    class Meta:
        model = WeldStoreList
        fields = ("count","item_status")
    def __init__(self,*args,**kwargs):
        super(WeldAccountItemForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields,"150px")

class SteelAccountItemForm(ModelForm):
    class Meta:
        model = SteelMaterialStoreList
        fields = ("specification","length","count","weight","store_room")
    def __init__(self,*args,**kwargs):
        super(SteelAccountItemForm,self).__init__(*args,**kwargs)
        self.fields["store_room"].queryset = StoreRoom.objects.filter(material_type = STOREROOM_CHOICES_STEEL)
        set_form_input_width(self.fields,"150px")

class OutsideAccountItemForm(ModelForm):
    class Meta:
        model = OutsideStorageList
        fields = ("count",)
    def __init__(self,*args,**kwargs):
        super(OutsideAccountItemForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields,"150px")

class AuxiliaryToolAccountItemForm(ModelForm):
    class Meta:
        model = AuxiliaryToolStoreList
        fields = ("count",)
    def __init__(self,*args,**kwargs):
        super(AuxiliaryToolAccountItemForm,self).__init__(*args,**kwargs)
        set_form_input_width(self.fields,"150px")

class WeldApplyKeeperForm(ModelForm):
    class Meta:
        model = WeldingMaterialApplyCard
        fields = ("actual_weight","actual_count","remark")
    def __init__(self,*args,**kwargs):
            super(WeldApplyKeeperForm,self).__init__(*args,**kwargs)
            set_form_input_width(self.fields,"150px")
            
class CardStatusStopForm(ModelForm):
    class Meta:
        model = CardStatusStopRecord
        fields = ("remark",)
        widgets = {
            "remark":forms.Textarea(attrs={"rows":5,})
        }
