# coding: UTF-8
from datetime import *
from django import  forms
from django.forms import ModelForm
from purchasing.models import Supplier, bidApply, qualityPriceCard, PurchasingEntry
from const import ORDERFORM_STATUS_CHOICES

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
