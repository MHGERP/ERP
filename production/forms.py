# coding: UTF-8
from const import *
from production import *
from django import forms
from django.forms import ModelForm
from const.models import WorkOrder
from const.models import Materiel
from datetime import *
from django.forms import ModelForm
from production.models import *
from techdata.models import Processing
from techdata.models import ProcessingName
from const.forms import WorkOrderForm
from django.contrib.auth.models import User

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

class SubWorkOrderForm(forms.Form):
    """
    LiuYe
    summary: store all work orders
    """
    sub_order = forms.ChoiceField(label=u"工作令", required = False, widget = forms.Select(attrs = {"class": "form-control input"}))
    def __init__(self, *args, **kwargs):
         super(SubWorkOrderForm, self).__init__(*args, **kwargs)
         WORKORDER_CHOICES = tuple([("", u"----------")]  + [(item.id, item) for item in SubWorkOrder.objects.all()])
         self.fields["sub_order"].choices = WORKORDER_CHOICES

        
class LedgerSearchForm(SubWorkOrderForm):
    materiel_belong__index__contains = forms.CharField(required=False, label=u"工作票号")
    materiel_belong__parent_schematic_index__contains = forms.CharField(required=False, label=u"部件图号")


class OrderIndexForm(forms.Form):
    order_index = forms.ChoiceField(widget = forms.Select(attrs = {'class': 'form-control input-medium'}))
    def __init__(self, *args, **kwargs):
        super(OrderIndexForm, self).__init__(*args, **kwargs)
        ORDER_INDEX_CHOICES = tuple((item.order_index,item.order_index) for item in WorkOrder.objects.all())
        self.fields["order_index"].choices = ORDER_INDEX_CHOICES

class TaskAllocationSearchForm(forms.Form):
    sub_materiel_belong__sub_order= forms.ChoiceField(required = False, widget = forms.Select(attrs = {'class': 'form-control input-medium '}),label=u"工作令")
    sub_materiel_belong__materiel_belong__index = forms.CharField(required=False, label=u"工作票号")
    processname__name = forms.ChoiceField(required=False, label=u"工序")
    productionworkgroup__name__contains = forms.CharField(required=False,label=u"操作组")
    def __init__(self, *args, **kwargs):
        super(TaskAllocationSearchForm, self).__init__(*args, **kwargs)
        ORDER_INDEX_CHOICES = tuple([("", u"----------")]  + [(item.id,item) for item in SubWorkOrder.objects.all()])
        self.fields["sub_materiel_belong__sub_order"].choices = ORDER_INDEX_CHOICES
        PROCESS_NAME_CHIOCES = tuple([("",u"----------")] + [(item.name,item.get_name_display()) for item in ProcessingName.objects.all()])
        self.fields["processname__name"].choices = PROCESS_NAME_CHIOCES

class TaskPlanForm(forms.Form):
    sub_materiel_belong__sub_order= forms.ChoiceField(required = False, widget = forms.Select(attrs = {'class': 'form-control input-medium '}),label=u"工作令")
    sub_materiel_belong__materiel_belong__index = forms.CharField(required=False, label=u"工作票号")
    processname__name = forms.ChoiceField(required=False, label=u"工序")
    plan_startdate__isnull = forms.ChoiceField(choices=TASK_PLAN_STATUS_CHOICES, required=False, label=u"任务计划状态")
    def __init__(self, *args, **kwargs):
        super(TaskPlanForm, self).__init__(*args, **kwargs)
        ORDER_INDEX_CHOICES = tuple([("", u"----------")]  + [(item.id,item) for item in SubWorkOrder.objects.all()])
        self.fields["sub_materiel_belong__sub_order"].choices = ORDER_INDEX_CHOICES
        PROCESS_NAME_CHIOCES = tuple([("",u"----------")] + [(item.name,item.get_name_display()) for item in ProcessingName.objects.all()])
        self.fields["processname__name"].choices = PROCESS_NAME_CHIOCES

class TaskAllocationForm(TaskAllocationSearchForm):
    productionworkgroup__isnull  = forms.ChoiceField(choices=TASK_ALLOCATION_STATUS_CHOICES, required=False, label=u"任务分配状态")

class TaskConfirmForm(TaskAllocationSearchForm):
    complete_process_date__isnull  = forms.ChoiceField(choices=TASK_CONFIRM_STATUS_CHOICES, required=False, label=u"任务完成状态")

class MaterialPlantimeChangeForm(ModelForm):
    class Meta:
        model = SubMateriel
        fields = {'materiel_belong','sub_order','complete_plandate'}
        widgets = { 
            "materiel_belong": forms.TextInput(attrs={"readonly":"true"}), 
            "sub_order": forms.TextInput(attrs={"readonly":"true"}), 
           # "complete_plandate" : forms.DateInput(attrs={"id":"complete_plandate"}),
        }

class DateForm(forms.Form):
    order_index = forms.ChoiceField(widget = forms.Select(attrs = {'class': 'form-control input-medium '}),label=u"工作令")
    operator = forms.ChoiceField(widget = forms.TextInput(attrs = {'class':'form-control input'}),label=u"操作员")
    date = forms.ChoiceField(widget = forms.Select(attrs = {'class':'form-control input-medium'}),label=u"日期")
class HourSummarizeForm(forms.Form):
    sub_materiel_belong__sub_order = forms.ChoiceField(required = False,widget = forms.Select(attrs = {'class': 'form-control input-medium '}),label=u"工作令")
    productionworkgroup = forms.ChoiceField(required=False, widget = forms.Select(attrs = {"class": "form-control input"}),label=u"组号")
    complete_process_date__gte = forms.DateField(label = u"完成时间开始", required = False)
    complete_process_date__lte = forms.DateField(label = u"完成时间结束", required = False)
    def __init__(self, *args, **kwargs):
        super(HourSummarizeForm, self).__init__(*args, **kwargs)
        WORKORDER_CHOICES = tuple([("", u"----------")]  + [(item.id, item) for item in SubWorkOrder.objects.all()])
        self.fields["sub_materiel_belong__sub_order"].choices = WORKORDER_CHOICES
        GROUO_NUM_CHOICES = tuple([("","------")]+[(item.id, item.name) for item in ProductionWorkGroup.objects.all()])
        self.fields["productionworkgroup"].choices = GROUO_NUM_CHOICES

class HourMessageSearchForm(forms.Form):
    sub_materiel_belong__sub_order = forms.ChoiceField(label=u"工作令", required = False, widget = forms.Select(attrs = {"class": "form-control input"}))
    sub_materiel_belong__materiel_belong__index__contains = forms.CharField(required=False, label=u"工作票号")
    productionworkgroup = forms.ChoiceField(required=False, widget = forms.Select(attrs = {"class": "form-control input"}),label=u"组号")
    def __init__(self, *args, **kwargs):
         super(HourMessageSearchForm, self).__init__(*args, **kwargs)
         GROUO_NUM_CHOICES = tuple([("","------")]+[(item.id, item.name) for item in ProductionWorkGroup.objects.all()])
         self.fields["productionworkgroup"].choices = GROUO_NUM_CHOICES
         WORKORDER_CHOICES = tuple([("", u"----------")]  + [(item.id, item) for item in SubWorkOrder.objects.all()])
         self.fields["sub_materiel_belong__sub_order"].choices = WORKORDER_CHOICES

class WorkGroupForm(forms.Form):
    production_work_group = forms.ChoiceField(required=False, widget = forms.Select(attrs = {"class": "form-control input"}),label=u"组号")
    def __init__(self, *args, **kwargs):
         super(WorkGroupForm, self).__init__(*args, **kwargs)
         self.fields["production_work_group"].choices = tuple([("","------")]+[(item.id, item.name) for item in ProductionWorkGroup.objects.all()])

class ProductionUserSearchForm(forms.Form):
    production_user_id__name__contains = forms.CharField(required=False, label=u"生产人员姓名",)
    production_work_group = forms.ChoiceField(required=False, widget = forms.Select(attrs = {"class": "form-control input"}),label=u"组号")
    def __init__(self, *args, **kwargs):
         super(ProductionUserSearchForm, self).__init__(*args, **kwargs)
         self.fields["production_work_group"].choices = tuple([("","------")]+[(item.id, item.name) for item in ProductionWorkGroup.objects.all()])

class UserChooseForm(forms.Form):
    name__contains = forms.CharField(label=u"用户姓名",required = False)


class ProductionUserForm(ModelForm):
    class Meta:
        model = ProductionUser
        fields = ("production_work_group",)
        widgets = {
            "production_work_group":forms.Select(attrs={"class":"form-control"}),
        }
    def __init__(self, *args, **kwargs):
        super(ProductionUserForm,self).__init__(*args,**kwargs)
        self.fields["production_work_group"].choices = tuple((item.id, item.name) for item in ProductionWorkGroup.objects.all()) 
