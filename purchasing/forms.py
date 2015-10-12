# coding: UTF-8
from datetime import *
from django import  forms
from django.forms import ModelForm
from const.models import Materiel
from purchasing.models import Supplier, bidApply, qualityPriceCard, PurchasingEntry, BidComment
from purchasing.models import Supplier, bidApply, qualityPriceCard, PurchasingEntry,ProcessFollowingInfo, MainMaterielExecuteDetail, SupportMaterielExecuteDetail
from const import MATERIEL_CHOICE
class SupplierForm(ModelForm):
    class Meta:
        model=Supplier
        field=('supplier_id','supplier_name')
        widgets={
            'supplier_id':forms.TextInput(),
            'supplier_name':forms.TextInput(),
        }


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
        exclude = ('id','bidform','entry_confirm')
        widgets = {
            'entry_time':forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd","id":"entry_time"}),
            'receipts_code':forms.TextInput(attrs={"id":"receipts_code"}),
            'purchaser':forms.TextInput(attrs={"readonly":"true",'class':'span3'}),
            'inspector':forms.TextInput(attrs={"readonly":"true",'class':'span3'}),
            'keeper':forms.TextInput(attrs={"readonly":"true",'class':'span3'}),

            
        }


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

"""
class SupportMaterielExecuteDetailForm(forms.Form):
    materiel_texture_choice = tuple((item.id, item) for item in Materiel.objects.all())
    materiel_texture = forms.ChoiceField(choices = materiel_texture_choice, label = u"材质", widget = forms.Select())
    texture_number = forms.CharField(required = True, label = u"材质编号", widget = forms.TextInput())
    specification = forms.CharField(required = True, label = u"规格", widget = forms.TextInput())
    quantity = forms.IntegerField(required = True, label = u"数量", widget = forms.TextInput())
    delivery_status = forms.CharField(required = True, label = u"交货状态", widget = forms.TextInput())
    press = forms.CharField(required = True, label = u"受压", widget = forms.TextInput())
    crack_rank = forms.CharField(required = True, label = u"探伤级别", widget = forms.TextInput())
    recheck_choice = (('0', '未复验'), ('1', '已复验'))
    recheck = forms.ChoiceField(required = True, label = u"复验", widget = forms.RadioSelect, choices = recheck_choice)
    quota = forms.CharField(required = False, label = u"定额", widget = forms.TextInput())
    part = forms.CharField(required = False, label = u"零件", widget = forms.TextInput())
    oddments = forms.CharField(required = False, label = u"余料", widget = forms.TextInput())
    remark = forms.CharField(required = False, label = u"备注", widget = forms.TextInput())

class MainMaterielExecuteDetailForm(forms.Form):
    materiel_texture_choice = tuple((item.id, item) for item in Materiel.objects.all())
    materiel_texture = forms.ChoiceField(choices = materiel_texture_choice, label = u"材质", widget = forms.Select())
    materiel_name = forms.CharField(required = True, label = u"名称", widget = forms.TextInput())
    quality_class = forms.CharField(required = True, label = u"质量分类", widget = forms.TextInput())
    specification = forms.CharField(required = True, label = u"规格", widget = forms.TextInput())
    quantity = forms.IntegerField(required = True, label = u"数量", widget = forms.TextInput())
    purchase_weight = forms.FloatField(required = True, label = u"采购", widget = forms.TextInput())
    recheck_choice = (('0', '未复验'), ('1', '已复验'))
    recheck = forms.ChoiceField(required = True, label = u"复验", widget = forms.RadioSelect, choices = recheck_choice)
    crack_rank = forms.CharField(required = True, label = u"探伤级别", widget = forms.TextInput())
    delivery_status = forms.CharField(required = True, label = u"交货状态", widget = forms.TextInput())
    execute_standard = forms.CharField(required = True, label = u"执行标准", widget = forms.TextInput())
    remark = forms.CharField(required = False, label = u"备注", widget = forms.TextInput())
"""
