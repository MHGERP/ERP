# coding: UTF-8
from datetime import *
from django import  forms
from django.forms import ModelForm
from storage.models import *
from const.models import Materiel
from const import ORDERFORM_STATUS_CHOICES, MATERIEL_CHOICE,STORAGEDEPARTMENT_CHOICES,STEEL_TYPE,STEEL,STORAGE_ENTRY_TYPECHOICES,MATERIAL_TYPE
from django.contrib.auth.models import User
from users.utility import getUserByAuthority
from users import STORAGE_KEEPER
from const.utils import getChoiceList,getDistinctSet

DEPARTMENT_CHOICES=STORAGEDEPARTMENT_CHOICES

def set_form_input_width(dict,style=("style","width:120px;")):
    """
    设定form的样式
    """
    for k , v in dict.items():
        v.widget.attrs[style[0]] = style[1]

class ApplyCardHistorySearchForm(forms.Form):
    workorder = forms.ChoiceField(label=u"工作令",required = False,widget=forms.Select(attrs={"id":"workorder","class":"form_control","select2":"true"}))
    weld_bead_number = forms.CharField(label=u"焊缝编号",required=False,widget=forms.TextInput(attrs={"class":"form_control"}))
    material_mark = forms.CharField(label=u"焊材牌号",required=False,widget=forms.TextInput(attrs={"class":"form_control"}))
    model_number = forms.CharField(label=u"型号",required=False,widget=forms.TextInput(attrs={"class":"form_control"}))
    specification = forms.CharField(label=u"规格",required=False,widget=forms.TextInput(attrs={"class":"form_control"}))
    #department = forms.CharField(label=u"领用单位",required=False,widget=forms.TextInput(attrs={"class":"form_control"}))
    #applycard_code = forms.CharField(label=u"领用单编号",required=False,widget=forms.TextInput(attrs={"class":"form_control"}))
    create_time__gte = forms.DateField(label=u"起始日期",required=False,widget=forms.TextInput(attrs={"class":'form_control','date_picker':"true"}))
    create_time__lte = forms.DateField(label=u"终止日期",required=False,widget=forms.TextInput(attrs={"class":'form_control','date_picker':"true"}))
    def __init__(self,*args,**kwargs):
        super(ApplyCardHistorySearchForm,self).__init__(*args,**kwargs)
        self.fields["workorder"].choices = getChoiceList(getDistinctSet(WeldingMaterialApplyCard,WorkOrder,'workorder'),'order_index')
        style = ("style","width:120px;margin-bottom:10px;")
        set_form_input_width(self.fields,style)
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
    date = forms.DateField(label = u"日期",required = False, widget = forms.TextInput(attrs={'class':'form-controli span2','id':'date'}))
    storeRoom = forms.ChoiceField(label = u"库房",required = False, widget = forms.Select(attrs={"class":'form-control span2','id':'storeRoom'}))
    storeMan = forms.ChoiceField(label = u"库管员",required = False, widget = forms.Select(attrs={"class":'form-control span2','id':'storeMan'}))
    def __init__(self,*args,**kwargs):
        storeRoom = StoreRoom.objects.all()
        super(HumSearchForm,self).__init__(*args,**kwargs)
        room_list = [(-1,u"--------")]
        for room in storeRoom:
            room_list.append((room.id,room.name))
        self.fields["storeRoom"].choices = tuple(room_list)
        self.fields["storeMan"].choices =  getChoiceList(getUserByAuthority(STORAGE_KEEPER),"userinfo")

class BakeRecordForm(ModelForm):
    class Meta:
        model = WeldingMaterialBakeRecord
        exclude = ("storeMan",)
        widgets = { 
            "remark": forms.Textarea(attrs = {"rows":"2","style":"width:600px"}),
            "date":forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd","id":"date"}),
            "intoheattime":forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd hh:ii","id":"intoheattime"}),
            "timefortemp":forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd hh:ii","id":"timefortemp"}),
            "tempfalltime":forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd hh:ii","id":"tempfalltime"}),
            "timeforremainheat":forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd hh:ii","id":"timeforremainheat"}),
            "usetime":forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd hh:ii","id":"usetime"}),
        }
    def __init__(self,*args,**kwargs):
        super(BakeRecordForm,self).__init__(*args,**kwargs)
        engineers = getUserByAuthority(STORAGE_KEEPER)
        engin_tuple = tuple([ (user.id,user.userinfo) for user in engineers ]) 
        self.fields["weldengineer"].choices = engin_tuple

class BakeSearchForm(forms.Form):
    date = forms.DateField(label = u"日期",required = False, widget = forms.TextInput(attrs={'class':'form-controli span2','id':'date'}))
    standardnum = forms.CharField(label = u"标准号",required = False, widget = forms.TextInput(attrs={"class":'form-control span2','id':'standardnum'}))
    weldengineer = forms.ChoiceField(label = u"焊接工程师",required = False, widget = forms.Select(attrs={"class":'form-control span2','id':'weldengineer'}))
    storeMan = forms.ChoiceField(label = u"库管员",required = False, widget = forms.Select(attrs={"class":'form-control span2','id':'storeMan'}))
    def __init__(self,*args,**kwargs):
        super(BakeSearchForm,self).__init__(*args,**kwargs)
        print  getChoiceList(getUserByAuthority(STORAGE_KEEPER),"userinfo")
        self.fields["weldengineer"].choices = getChoiceList(getUserByAuthority(STORAGE_KEEPER),"userinfo")
        self.fields["storeMan"].choices =  getChoiceList(getUserByAuthority(STORAGE_KEEPER),"userinfo")

class ApplyRefundSearchForm(forms.Form):
    order_index = forms.CharField(label = u"工作令",required = False, widget = forms.TextInput(attrs={"class":'form-control span2','id':'order_index'}))
    product_name = forms.CharField(label = u"产品名称",required = False, widget = forms.TextInput(attrs={"class":'form-control span2','id':'product_name'}))

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
    remark = forms.CharField(label=u'备注',required=False,widget=forms.TextInput(attrs={'class':'form-control span2',}))
    store_room = forms.ChoiceField(widget = forms.Select(attrs = {'class': 'form-control input-medium span3'}),label = u"库房位置")
    def __init__(self, *args, **kwargs):
        super(steelEntryItemsForm, self).__init__(*args, **kwargs)
        STORE_ROOM_CHOICES = tuple([(item.id,item.name) for item in StoreRoom.objects.all()])
        self.fields["store_room"].choices = STORE_ROOM_CHOICES 

class RefundSearchForm(forms.Form):
    apply_card__workorder=forms.ChoiceField(label=u'工作令',required=False,widget=forms.Select(attrs={'class':'form-control span2','id':'work_order',"select2":"true"}))
    apply_card__weld_bead_number=forms.CharField(label=u'焊缝编号',required=False,widget=forms.TextInput(attrs={'class':'form-control span2','id':'work_order'}))
    create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control','date_picker':'true',}))
    create_time__lte = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control','date_picker':'true',}))
    def __init__(self,*args,**kwargs):
        super(RefundSearchForm,self).__init__(*args,**kwargs)
        style = ("style","width:120px;")
        set_form_input_width(self.fields,style)
        workorder_list = WorkOrder.objects.all()
        self.fields["apply_card__workorder"].choices = getChoiceList(workorder_list,"order_index")
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
    department=forms.CharField(label=u'领用人',required=False,widget=forms.TextInput(attrs={'class':'form-control',}))
    applycard_code=forms.CharField(label=u'编号',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))


class AuxiliaryEntrySearchForm(forms.Form):
    create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control','date_picker':'true'}))
    create_time__lte  = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control', 'date_picker':'true'}))
    entry_code=forms.CharField(label=u'入库单编号',required=False,widget=forms.TextInput(attrs={'class':'form-control date_picker','id':'entry_code'}))

    
    def __init__(self, *args, **kwargs):
        super(AuxiliaryEntrySearchForm, self).__init__(*args, **kwargs)
        style = ("style","width:120px;")
        set_form_input_width(self.fields,style)

class SteelRefundSearchForm(forms.Form):
    date = forms.DateField(label=u"日期",required = False,widget=forms.TextInput(attrs={"class":'form-control span2','id':'date'}))
    form_code = forms.CharField(label=u'编号',required=False,widget=forms.TextInput(attrs={'class':'form-control span2','id':'form_code'}))
    work_order=forms.ChoiceField(label=u'工作令',required=False,widget=forms.Select(attrs={'class':'form-control span2','id':'work_order'}))
    # keeper=forms.ChoiceField(label=u'库管员',required=False,widget=forms.Select(attrs={'class':'form-control span2','id':'keeper'}))
    def __init__(self,*args,**kwargs):
        super(SteelRefundSearchForm,self).__init__(*args,**kwargs)
        # users = getUserByAuthority(STORAGE_KEEPER)
        # self.fields["keeper"].choices = getChoiceList(users,"userinfo")

        workorder_list = CommonSteelMaterialApplyCardInfo.objects.values("work_order").distinct()
        work_order_set = []
        for list_tmp in workorder_list:
            work_order_set.append(WorkOrder.objects.get(id = list_tmp["work_order"]))
        self.fields["work_order"].choices = getChoiceList(work_order_set,"order_index")

class WeldStorageSearchForm(forms.Form):
    material_id = forms.CharField(label=u'材质编号',required=False,widget=forms.TextInput(attrs={'class':'form-control search-in','id':'material_id'}))
    brand=forms.CharField(label=u'牌号',required=False,widget=forms.TextInput(attrs={'class':'form-control search-in','id':'brand'}))
    specification=forms.CharField(label=u'规格',required=False,widget=forms.TextInput(attrs={'class':'form-control search-in','id':'specification'}))
    charge_number=forms.CharField(label=u'材料批号',required=False,widget=forms.TextInput(attrs={'class':'form-control search-in','id':'charge_number'}))

class WeldAccountSearchForm(WeldStorageSearchForm):
    entry_time = forms.DateField(label=u"日期",required = False,widget=forms.TextInput(attrs={"class":'form-control search-in','id':'entry_time'}))

class WeldApplyAccountSearchForm(forms.Form):
    workorder = forms.ChoiceField(label=u"工作令",required = False,widget=forms.Select(attrs={"class":'form-control search-in','id':'workorder'}))
    weld_bead_number = forms.CharField(label=u"焊缝编号",required = False,widget=forms.TextInput(attrs={"class":'form-control search-in','id':'weld_bead_number'}))
    index = forms.CharField(label=u"编号",required = False,widget=forms.TextInput(attrs={"class":'form-control search-in','id':'index'}))
    create_time = forms.DateField(label=u"日期",required = False,widget=forms.TextInput(attrs={"class":'form-control search-in','id':'create_time'}))
    def __init__(self,*args,**kwargs):
        super(WeldApplyAccountSearchForm,self).__init__(*args,**kwargs)
        workorder_list = WeldingMaterialApplyCard.objects.values("workorder").distinct()
        work_order_set = []
        for list_tmp in workorder_list:
            work_order_set.append(WorkOrder.objects.get(id = list_tmp["workorder"]))
        self.fields["workorder"].choices = getChoiceList(work_order_set,"order_index")

class SteelLedgerSearchForm(forms.Form):
    steel_type = forms.ChoiceField(label=u"钢材类型",required=False,widget=forms.Select(attrs={"class":'form-control'}))
    store_room = forms.ChoiceField(label=u"库房",required=False,widget=forms.Select(attrs={"class":"form-control"}))
    material_number = forms.CharField(label=u"材质编号",required=False,widget=forms.TextInput(attrs={"class":"form-control"}))
    # is_returned = forms.ChoiceField(label=u"是否被退库",required=False,widget=forms.Select(attrs={"class":"form-control"}))

    def __init__(self,*args,**kwargs):
        super(SteelLedgerSearchForm,self).__init__(*args,**kwargs)
        self.fields["steel_type"].choices = STEEL_TYPE
        storerooms = StoreRoom.objects.filter(material_type=STEEL)
        storeroom_choice=[(-1,'')]
        for storeroom in storerooms:
            storeroom_choice.append((storeroom.id,storeroom.name))
        self.fields['store_room'].choices = storeroom_choice
        return_choice = [(-1,""),(False,'未退库'),(True,'退库过')]
        # self.fields['is_returned'].choices=return_choice

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
        workorders = getDistinctSet(OutsideApplyCard,WorkOrder,'workorder')
        proposers = getDistinctSet(OutsideApplyCard,User,'proposer')
        self.fields['workorder'].choices = getChoiceList(workorders,'order_index')
        self.fields['proposer'].choices = getChoiceList(proposers,'userinfo')

class OutsideApplyCardForm(ModelForm):
    class Meta:
        model = OutsideApplyCard
        fields = ("change_code","sample_report","entry_code")
    def __init__(self,*args,**kwargs):
        super(OutsideApplyCardForm,self).__init__(*args,**kwargs)

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
        workorders = getDistinctSet(WorkOrder,WorkOrder,'id')
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
        self.fields["work_order"].choices = getChoiceList(getDistinctSet(OutsideApplyCard,WorkOrder,'workorder',entry_status=STORAGESTATUS_END),'order_index')


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
        self.fields["material_type"].choices = MATERIAL_TYPE


class StoreRoomSearchForm(forms.Form):
    name = forms.CharField(label=u"库房名称",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    position = forms.CharField(label=u"位置",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    material_type = forms.ChoiceField(label=u"材料类型",required = False, widget = forms.Select(attrs={"class":'form-control'}))

    def __init__(self,*args,**kwargs):
        super(StoreRoomSearchForm, self).__init__(*args, **kwargs)
        type_list = [(-1, u"---------"),]
        type_list.extend(list(MATERIAL_TYPE))

        self.fields["material_type"].choices = tuple(type_list)

class CheckMaterielDbForm(forms.Form):
    db_type = forms.ChoiceField(label=u"材料类型",required = True,choices = MATERIEL_TYPE_CHOICES,widget = forms.Select(attrs={'class':"span2","id":"db_type"}))

class CheckMaterielListForm(forms.Form):
    materiel_type = forms.ChoiceField(label=u"库存材料",required = False, widget=forms.Select(attrs={'id':'materiel_type','class':"span2",'select2':'true'}))
    def __init__(self,*args,**kwargs):
        db_type = kwargs.pop("db_type",WeldStoreList)
        super(CheckMaterielListForm,self).__init__(*args,**kwargs)
        if db_type != None:
            materiels =objects.all()
            self.fields['materiel_type'].choices = getChoiceList(materiels,'specification')

class WeldEntrySearchForm(forms.Form):
    create_time__gte = forms.DateField(label=u"起始日期",required = False,widget=forms.TextInput(attrs={"class":'form-control date_picker','date_picker':'true'}))
    create_time__lte  = forms.DateField(label=u"终止日期",required = False,widget=forms.TextInput(attrs={"class":'form-control date_picker', 'date_picker':'true'}))
    entry_code=forms.CharField(label=u'入库单编号',required=False,widget=forms.TextInput(attrs={'class':'form-control date_picker','id':'entry_code'}))

class WeldApplyKeeperForm(ModelForm):
    class Meta:
        model = WeldingMaterialApplyCard
        fields = ("actual_weight","actual_quantity","remark")
        widgets={
                'actual_weight':forms.TextInput(attrs={'class':'span2'}),
                'actual_quantity':forms.TextInput(attrs={'class':'span2'}),
                'remark':forms.TextInput(attrs={'class':'span2'}),
        }
class WeldMaterialSearchForm(forms.Form):
    material__name = forms.CharField(label=u"名称",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    material_mark = forms.CharField(label=u"牌号",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    model_number = forms.CharField(label=u"型号",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    specification = forms.CharField(label=u"规格",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))
    factory = forms.CharField(label=u"厂家",required = False, widget = forms.TextInput(attrs={"class":'form-control'}))

class WeldRefundConfirmForm(ModelForm):
    class Meta:
        model = WeldRefund
        fields = ("refund_weight","refund_status")
