# coding: UTF-8
from const import *
from django import forms
from django.forms import ModelForm
from const.models import WorkOrder
from datetime import *
from django.forms import ModelForm
from production.models import ProductionPlan
from techdata.models import Processing
from const.forms import WorkOrderForm

class ProductionPlanForm(ModelForm):
    class Meta:
        model = ProductionPlan
        exclude = ('plan_id', )

class ProductionPlanSearchForm(WorkOrderForm):
    status = forms.ChoiceField(label=u"状态", choices=PRODUCTION_PLAN_STAUTS_CHOICES)
    plan_date = forms.ChoiceField(label=u"计划年月")
    def __init__(self, *args, **kwargs):
        super(ProductionPlanSearchForm, self).__init__(*args, **kwargs)
        DATE_CHOICE = tuple(("%s-%s"%(item.year,item.month),"%s-%s"%(item.year,item.month)) for item in ProductionPlan.objects.dates('plan_date', 'month').distinct())
        self.fields["plan_date"].choices = DATE_CHOICE

class LedgerSearchForm(WorkOrderForm):
    work_index = forms.CharField(required=False, label=u"工作票号")
    parent_schematic = forms.CharField(required=False, label=u"部件图号")


class OrderIndexForm(forms.Form):
    order_index = forms.ChoiceField(widget = forms.Select(attrs = {'class': 'form-control input-medium'}))
    def __init__(self, *args, **kwargs):
        super(OrderIndexForm, self).__init__(*args, **kwargs)
        ORDER_INDEX_CHOICES = tuple((item.order_index,item.order_index) for item in WorkOrder.objects.all())
        self.fields["order_index"].choices = ORDER_INDEX_CHOICES

class TaskAllocationSearchForm(forms.Form):
    workorder_choices=tuple([(-1,"------")]+[(item.id,item.order_index) for item in WorkOrder.objects.all()])
    workorder=forms.ChoiceField(choices=workorder_choices,required=False)
    identifier=forms.CharField(required=False)
    processnumber=forms.CharField(required=False)
    groupnumber=forms.CharField(required=False)

class DateForm(forms.Form):
    order_index = forms.ChoiceField(widget = forms.Select(attrs = {'class': 'form-control input-medium '}),label=u"工作令")
    operator = forms.ChoiceField(widget = forms.TextInput(attrs = {'class':'form-control input'}),label=u"操作员")
    date = forms.ChoiceField(widget = forms.Select(attrs = {'class':'form-control input-medium'}),label=u"日期")

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        ORDER_INDEX_CHOICES = tuple((item.order_index,item.order_index) for item in WorkOrder.objects.all())
        self.fields["order_index"].choices = ORDER_INDEX_CHOICES
        DATE_CHOICE = tuple(("%s-%02d"%(item.year,item.month),"%s-%02d"%(item.year,item.month)) for item in Processing.objects.dates('operate_date', 'month').distinct())
        self.fields["date"].choices = DATE_CHOICE

class HourMessageSearchForm(forms.Form):
    order_index = forms.ChoiceField(widget = forms.Select(attrs = {'class': 'form-control input-medium'}),label=u"工作令")
    work_ticket = forms.ChoiceField(widget = forms.TextInput(attrs = {'class':'form-control input'}),label=u"工作票号")
    group_num = forms.ChoiceField(widget = forms.TextInput(attrs = {'class':'form-control input'}),label=u"组号")
    
    def __init__(self, *args, **kwargs):
        super(HourMessageSearchForm, self).__init__(*args, **kwargs)
        ORDER_INDEX_CHOICES = tuple((item.order_index,item.order_index) for item in WorkOrder.objects.all())
        self.fields["order_index"].choices = ORDER_INDEX_CHOICES
