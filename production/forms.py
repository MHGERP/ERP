# coding: UTF-8
from const import *
from production import *
from django import forms
from django.forms import ModelForm
from const.models import WorkOrder
from datetime import *
from django.forms import ModelForm
from production.models import ProductionPlan,ProductionWorkGroup
from techdata.models import Processing
from const.forms import WorkOrderForm

class WorkOrderProductionForm(forms.Form):
    """
    LiuYe
    summary: store all work orders
    """
    order = forms.ChoiceField(label=u"工作令", required = False, widget = forms.Select(attrs = {"class": "form-control input"}))
    def __init__(self, *args, **kwargs):
         super(WorkOrderProductionForm, self).__init__(*args, **kwargs)
         WORKORDER_CHOICES = tuple([("", u"----------")]  + [(item.id, item) for item in WorkOrder.objects.all()])
         self.fields["order"].choices = WORKORDER_CHOICES

class WorkOrderProductionSearchForm(forms.Form):
    """
    LiuYe
    summary: search work order fuzzy
    """
    order_index__contains = forms.CharField(required=False, label=u"工作令")

class ProductionPlanSearchForm(WorkOrderProductionForm):
    status = forms.ChoiceField(label = u"状态", required = False, choices=PRODUCTION_PLAN_STAUTS_CHOICES)
    plan_date__gte = forms.DateField(label = u"计划年月开始", required = False)
    plan_date__lte = forms.DateField(label = u"计划年月终止", required = False)

class ProdPlanForm(ModelForm):
    class Meta:
        model = ProductionPlan
        exclude = ("order","plan_id",)
        widgets = {
            "plan_date":forms.DateInput(attrs={"data-date-format":"yyyy-mm-dd","id":"plan_date"}),
            "status":forms.Select(attrs={"class":"form-control"}),
        }
    def __init__(self, *args, **kwargs):
        super(ProdPlanForm,self).__init__(*args,**kwargs)
        self.fields["plan_date"].choices = PRODUCTION_PLAN_STAUTS_CHOICES


class LedgerSearchForm(WorkOrderProductionForm):
    index__contains = forms.CharField(required=False, label=u"工作票号")
    parent_schematic_index__contains = forms.CharField(required=False, label=u"部件图号")


class OrderIndexForm(forms.Form):
    order_index = forms.ChoiceField(widget = forms.Select(attrs = {'class': 'form-control input-medium'}))
    def __init__(self, *args, **kwargs):
        super(OrderIndexForm, self).__init__(*args, **kwargs)
        ORDER_INDEX_CHOICES = tuple((item.order_index,item.order_index) for item in WorkOrder.objects.all())
        self.fields["order_index"].choices = ORDER_INDEX_CHOICES

class TaskAllocationSearchForm(forms.Form):
    workorder_choices=tuple([(-1,"------")]+[(item.id,item.order_index) for item in WorkOrder.objects.all()])
    workorder=forms.ChoiceField(choices=workorder_choices,required=False, label=u"工作令")
    identifier=forms.CharField(required=False, label=u"编号")
    processnumber=forms.CharField(required=False, label=u"工序号")
    groupnumber=forms.CharField(required=False,label=u"操作组")

class TaskAllocationForm(TaskAllocationSearchForm):
    task_allocation_status = forms.ChoiceField(choices=TASK_ALLOCATION_STATUS_CHOICES, required=False, label=u"任务分配状态")

class TaskConfirmForm(TaskAllocationSearchForm):
    task_confirm_status = forms.ChoiceField(choices=TASK_CONFIRM_STATUS_CHOICES, required=False, label=u"任务完成状态")

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
    materiel_belong__order = forms.ChoiceField(label=u"工作令", widget = forms.Select(attrs = {"class": "form-control input"}))
    materiel_belong__index__contains = forms.CharField(required=False, label=u"工作票号")
    productionworkgroup__name = forms.ChoiceField(required=False, widget = forms.Select(attrs = {"class": "form-control input"}),label=u"组号")
    def __init__(self, *args, **kwargs):
         super(HourMessageSearchForm, self).__init__(*args, **kwargs)
         GROUO_NUM_CHOICES = tuple([("","------")]+[(item.id, item.name) for item in ProductionWorkGroup.objects.all()])
         self.fields["productionworkgroup__name"].choices = GROUO_NUM_CHOICES
         WORKORDER_CHOICES = tuple((item.id, item) for item in WorkOrder.objects.all())
         self.fields["materiel_belong__order"].choices = WORKORDER_CHOICES

