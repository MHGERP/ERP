# coding: UTF-8
from datetime import *
from django import  forms
from django.forms import ModelForm
from purchasing.models import *
from const import ORDERFORM_STATUS_CHOICES
from const.models import Materiel
from const import ORDERFORM_STATUS_CHOICES, MATERIEL_CHOICE, RECHECK_CHOICE
from purchasing.models import MaterielCopy
from storage.models import *

class SupplierForm(ModelForm):
    class Meta:
        model=Supplier
        field=('supplier_id','supplier_name')
        widgets={
            'supplier_id':forms.TextInput(),
            'supplier_name':forms.TextInput(),
        }

class OrderFormStatusForm(forms.Form):
    """
    JunHU
    summary: store all step of order form status
    """
    status = forms.ChoiceField(choices = ORDERFORM_STATUS_CHOICES, widget = forms.Select(attrs = {'class': 'form-control input'}))


class BidApplyForm(ModelForm):
    class Meta:
        model = bidApply
        fields = ('apply_company', 'demand_company', 'bid_project', 'bid_date', 'project_category', 'work_order', 'special_model', 'amount', 'core_part')
        widgets = {
                   "bid_date": forms.DateInput(attrs={'class':'form-control'}),
                  }
class BidApplySupplierForm(ModelForm):
    class Meta:
        model=SupplierSelect
        fields=("supplier_code","sphere")


class BidLogisticalForm(ModelForm):
    class Meta:
        model = bidApply
        fields = ("apply_id","bid_delivery_date","bid_datetime","place","implement_class")
        widgets = {
            "bid_delivery_date":forms.DateInput(attrs={'class':'form-control'}),
            "bid_datetime":forms.DateInput(attrs={'class':'form-control'})
                  }

class SupplierCheckForm(ModelForm):
    class Meta:
        model=SupplierCheck
        fields=("apply_company","apply_date","bid_project","price_estimate","base_situation")
        widgets = {
                   "apply_date": forms.DateInput(attrs={'class':'form-control'}),
                  }

class SupplierCheckSupplierForm(ModelForm):
    class Meta:
        model=SupplierSelect
        fields=("A","B","C","D","E","F","G")

class QualityPriceCardForm(ModelForm):
    class Meta:
        model = qualityPriceCard
        fields=("apply_company","work_order","amount","unit","content","material","delivery_period")
        widgets = {
                   "apply_date": forms.DateInput(attrs={'class':'form-control'}),
                  }

class QualityCardSupplierForm(ModelForm):
    class Meta:
        model=SupplierSelect
        fields=("price","ability_situation","delivery_payment")
class ContractDetailForm(ModelForm):
    class Meta:
        model = ContractDetail
        fields = ('amount', )

class BidCommentForm(forms.Form):
    result_choices=(("-1","请审核"),("0","通过"),("1","不通过"))
    judgeresult =forms.ChoiceField(choices=result_choices,required=True, label=u"审核结果",
        widget=forms.Select(attrs={
            'class':'form-control',
            }),
        )
    reason=forms.CharField(required=False, label=u"审核意见",  widget=forms.Textarea(attrs={'class':'form-control','row':10}))


class ProcessFollowingForm(ModelForm):
    class Meta:
        model=ProcessFollowingInfo
        widgets={
            "following_feedback":forms.Textarea(attrs={"rows":5})
        }

class QualityCheckAddForm(ModelForm):
    class Meta:
        model = MaterielCopy
        fields = ('batch_number',"quality_number" )

# class MaterielChoiceForm(forms.Form):
#     materiel_chice_select = forms.ChoiceField(choices=MATERIEL_CHOICE, required=True, label=u"材料选择", widget = forms.Select(attrs={"id" : "materiel_choice_select"}))

class MaterielExecuteForm(ModelForm):
    class Meta:
        model = MaterielExecute
        exclude = {'id', 'document_lister', 'date', 'is_save','tech_feedback','tech_requirement'}
        widgets = {
            'materiel_choice' : forms.Select(attrs={"id" : "materiel_choice_select"})
        }
"""
class MainMaterielExecuteDetailForm(ModelForm):
    class Meta:
        model = MainMaterielExecuteDetail
        exclude = ('id', 'materiel_execute')
        widgets = {
            'recheck' : forms.RadioSelect(choices = (('0', '未复验'), ('1', '已复验')))
        }

class SupportMaterielExecuteDetailForm(ModelForm):
    class Meta:
        model = SupportMaterielExecuteDetail
        exclude = ('id', 'materiel_execute')
        widgets = {
            'recheck' : forms.RadioSelect(choices = (('0', '未复验'), ('1', '已复验')))
        }
"""

class SubApplyForm(ModelForm):
    class Meta:
        model = MaterialSubApply
        exclude = ('id','is_submit','proposer','comments','is_approval')
        widgets = {
            "reasons":forms.Textarea(attrs={'cols':'80','rows':'5'}),
        }

class SubApplyInspectForm(ModelForm):
    class Meta:
        model = MaterialSubApply
        exclude = ('id','is_submit','proposer')
        widgets = {
            "reasons":forms.Textarea(attrs={'cols':'80','rows':'5'}),
            "comments":forms.Textarea(attrs={'cols':'80','rows':'5'})
        }
class SubApplyItemForm(ModelForm):
    class Meta:
        model = MaterialSubApplyItems
        exclude = ('id','sub_apply')

class StatusChangeApplyForm(ModelForm):
    class Meta:
        model = StatusChange
        exclude = ('id','bidform','original_status','change_user','change_time','normal_change')
    def __init__(self,*args,**kwargs):
        bidform = kwargs.pop("bidform",None)
        super(StatusChangeApplyForm,self).__init__(*args,**kwargs)
        self.fields["bidform"].widget.attrs["value"] = bidform.bid_id
        self.fields["origin_status"].widget.attrs["value"] = bidform.bid_status

    bidform = forms.CharField(label=u"标单编号",widget = forms.TextInput(attrs={'readonly':'readonly','id':'bidform'}))
    origin_status = forms.CharField(label=u"当前状态",widget=forms.TextInput(attrs={'readonly':'readonly','id':'origin_status'}))
    reason = forms.CharField(label=u"回溯原因",widget=forms.Textarea(attrs={'id':'reason','cols':'80','rows':'5'}))


class BidAcceptanceForm(ModelForm):
    class Meta:
        model=BidAcceptance
        exclude=('bid')
    def __init__(self,*args,**kwargs):
        bidform=kwargs.pop("bidform",None)
        super(BidAcceptanceForm,self).__init__(*args,**kwargs)
        if bidform != None:
            choice=[(item.supplier.id,item.supplier.supplier_name) for item in bidform.supplierselect_set.all()]
            choice=tuple(choice)
            self.fields["accept_supplier"].choices=choice


class OrderInfoForm(ModelForm):
    class Meta:
        model = Materiel
        fields = {'index','name','schematic_index',}
        widgets = {'index':forms.TextInput(attrs={"class":'form-control',"readonly":'readonly'}),
                   'name':forms.TextInput(attrs={"class":'form-control'}),
                   'schematic_index':forms.TextInput(attrs={"class":'form-control'}),
                   }

class MeterielExcecuteForm(ModelForm):
    class Meta:
        model = MaterielExecuteDetail
        fields = {'quota','part','oddments','remark',}
        widgets = {
            'quota':forms.TextInput(attrs={'class':'form-control','id':'quota'}),
            'part':forms.TextInput(attrs={'class':'form-control','id':'part'}),
            'oddments':forms.TextInput(attrs={'class':'form-control','id':'oddments'}),
            'remark':forms.TextInput(attrs={'class':'form-control','id':'remark'})
        }



class OrderFormOne(ModelForm):
    class Meta:
        model=MaterielCopy
        fields={'index','name','material','specification','press','recheck','remark','standard','detection_level','count','total_weight','status'}

class OrderFormTwo(ModelForm):
    class Meta:
        model=MaterielCopy
        fields={'index','name','schematic_index','material','count','remark'}

class OrderFormThree(ModelForm):
    class Meta:
        model=MaterielCopy
        fields={'name','specification','material','quota','remark','standard'}

class EntryTypeForm(forms.Form):
    entry_type=forms.ChoiceField(label=u'入库单类型',choices=(),required=True,widget=forms.Select(attrs={'class':'form-control span2','id':'entry_type'}))
    def __init__(self,*args,**kwargs):
        bidform=kwargs.pop("bidform",None)
        super(EntryTypeForm,self).__init__(*args,**kwargs)
        if bidform != None:
            ENTRYTYPE_BOARD=("entrytype_board",u"板材")
            ENTRYTYPE_BAR=("entrytrpe_bar",u"型材")
            STANDARD_OUTSIDEBUY=("standard_outsidebuy",u"标准件")
            FORGING_OUTSIDEBUY=("forging",u"锻件")
            COOPERATION_OUTSIDEBUY=("cooperation_outsidebuy",u"外协加工")
            WELDING=("welding",u"焊材")
            AUXILIARY_TOOL=("auxiliary",u"辅助工具")
            if bidform.order_form.order_mod == 0:
                self.fields["entry_type"].choices=(ENTRYTYPE_BOARD,ENTRYTYPE_BAR)
            elif bidform.order_form.order_mod == 1:
                self.fields["entry_type"].choices=(ENTRYTYPE_BOARD,ENTRYTYPE_BAR,STANDARD_OUTSIDEBUY,FORGING_OUTSIDEBUY,COOPERATION_OUTSIDEBUY)
            elif bidform.order_form.order_mod == 2:
                self.fields["entry_type"].choices=(WELDING)


class WeldEntryForm(ModelForm):
    class Meta:
        model=WeldMaterialEntryItems
        fields={"price","total_weight","single_weight","production_date","factory","count","material_charge_number","model_number","remark"}

class SteelEntryForm(ModelForm):
    class Meta:
        model=SteelMaterialEntryItems
        fields={"weight","unit","store_room","length","material_code","batch_number"}
class AuxiliaryEntryForm(ModelForm):
    class Meta:
        model=AuxiliaryToolEntryItems
        fields={"unit","factory","supplier","remark"}
class OutsideEntryForm(ModelForm):
    class Meta:
        model=OutsideStandardItems
        fields={"material_code","batch_number","unit","weight","count","heatnum","factory","remark"}
