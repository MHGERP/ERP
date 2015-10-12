# coding: UTF-8
from datetime import *
from django import  forms
from django.forms import ModelForm
from purchasing.models import Supplier,PurchasingEntry,MaterialSubApply,MaterialSubApplyItems,\
        bidApply, qualityPriceCard,BidComment, ProcessFollowingInfo, MainMaterielExecuteDetail, SupportMaterielExecuteDetail
from const.models import Materiel
from const import ORDERFORM_STATUS_CHOICES, MATERIEL_CHOICE

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


class QualityPriceCardForm(ModelForm):
    class Meta:
        model = qualityPriceCard


class BidCommentForm(forms.Form):
    result_choices=(("-1","请审核"),("1","通过"),("0","不通过"))
    judgeresult =forms.ChoiceField(choices=result_choices,required=True, label=u"审核结果",
        widget=forms.Select(attrs={
            'class':'form-control',
            }),
        )
    reason=forms.CharField(required=False, label=u"审核意见",  widget=forms.Textarea(attrs={'class':'form-control','row':10}))


class EntryForm(ModelForm):
    class Meta:
        model = PurchasingEntry
        fields = ('entry_time','receipts_code')
        widgets = {
            'entry_time':forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd","id":"entry_time"}),
            'receipts_code':forms.TextInput(attrs={"id":"receipts_code"}),
        }
    def __init__(self,*args,**kwargs):
        super(EntryForm,self).__init__(*args,**kwargs)
        pur_entry = kwargs["instance"]
        self.fields['purchaser'].widget.attrs["value"] = pur_entry.purchaser.username
        self.fields['keeper'].widget.attrs["value"] = pur_entry.purchaser.username
        self.fields['inspector'].widget.attrs["value"] = pur_entry.purchaser.username
    purchaser = forms.CharField(label=u"采购员",widget = forms.TextInput(attrs={'readonly':'readonly','id':'purchaser'}))
    inspector = forms.CharField(label=u"采购员",widget = forms.TextInput(attrs={'readonly':'readonly','id':'inspector'}))
    keeper = forms.CharField(label=u"采购员",widget = forms.TextInput(attrs={'readonly':'readonly','id':'keeper'}))
class ProcessFollowingForm(ModelForm):
    class Meta:
        model=ProcessFollowingInfo
        widgets={
            "following_feedback":forms.Textarea(attrs={"rows":5})
        }

class MaterielChoiceForm(forms.Form):
    materiel_chice_select = forms.ChoiceField(choices=MATERIEL_CHOICE, required=True, label=u"材料选择", widget = forms.Select(attrs={"id" : "materiel_choice_select"}))

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
