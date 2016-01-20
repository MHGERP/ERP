# coding: UTF-8
from datetime import *
from django import  forms
from django.forms import ModelForm
from purchasing.models import *
from const import ORDERFORM_STATUS_CHOICES
from const.models import Materiel
from const import ORDERFORM_STATUS_CHOICES, MATERIEL_CHOICE, RECHECK_CHOICE

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

class QualityPriceCardForm(ModelForm):
    class Meta:
        model = qualityPriceCard

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
        fields = {'batch_number','quota','part','oddments','remark',}
        widgets = {
            'batch_number':forms.TextInput(attrs={'class':'form-control','id':'batch_number'}),
            'quota':forms.TextInput(attrs={'class':'form-control','id':'quota'}),
            'part':forms.TextInput(attrs={'class':'form-control','id':'part'}),
            'oddments':forms.TextInput(attrs={'class':'form-control','id':'oddments'}),
            'remark':forms.TextInput(attrs={'class':'form-control','id':'remark'})
        }
