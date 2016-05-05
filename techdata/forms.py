#!/usr/bin/env python
# coding=utf-8
from django import  forms
from const.models import Materiel
from techdata.models import *
from const import PROCESSING_CHOICES, TRANSFER_CARD_TYPE_CHOICES,MATERIAL_CATEGORY_CHOICES

class MaterielForm(forms.ModelForm):
    """
    JunHU
    parent_schematic_index was exclude from "exclude" 2016.3.18
    """
    class Meta:
        model = Materiel
        exclude = ("id", "order",)
        widgets = {
            "name": forms.TextInput(attrs = {"class": "input-medium", "readonly": "true"}),
            "index": forms.TextInput(attrs = {"class": "input-medium", "readonly": "true"}),
            "sub_index": forms.TextInput(attrs = {"class": "input-medium", "readonly": "true"}),
            "schematic_index": forms.TextInput(attrs = {"class": "input-medium", "readonly": "true"}),
            "parent_schematic_index" : forms.TextInput(attrs = {"class" : "input-medium"}),
            "material": forms.Select(attrs = {"class": "input-medium", "readonly": "true"}),
            "count": forms.TextInput(attrs = {"class": "input-medium", "readonly": "true"}),
            "remark": forms.TextInput(attrs = {"class": "input-medium", "readonly": "true"}),
            "net_weight": forms.TextInput(attrs = {"class": "input-medium", "readonly": "true"}),
            "total_weight": forms.TextInput(attrs = {"class": "input-medium", "readonly": "true"}),
            "specification": forms.TextInput(attrs = {"class": "input-medium"}),
        }

class ProcessReviewForm(forms.ModelForm):
    """
    MH Chen
    """
    class Meta:
        model = ProcessReview
        exclude = ("materiel")
        widgets = {
            "problem_statement": forms.Textarea(attrs = {"rows":"5","style":"resize: none;width:300px"}),
            "advice_statement": forms.Textarea(attrs = {"rows":"5","style":"resize: none;width:300px"}),
            # "materiel":forms.CharField( )
        }

    
class ProcessingForm(forms.Form):
    """
    JunHU
    """
    process = forms.ChoiceField(choices = PROCESSING_CHOICES, widget = forms.Select(attrs = {"class": "input-medium"}))

class WeldSeamForm(forms.ModelForm):
    """
    JunHU
    """
    class Meta:
        model = WeldSeam
        exclude = ('materiel_belong',)
        widgets = {
            "weld_index": forms.TextInput(attrs = {"class": "input-small"}),
            "base_metal_thin_1": forms.TextInput(attrs = {"class": "input-small"}),
            "base_metal_thin_2": forms.TextInput(attrs = {"class": "input-small"}),
            "length": forms.TextInput(attrs = {"class": "input-small"}),
            "weight_1": forms.TextInput(attrs = {"class": "input-small"}),
            "weight_2": forms.TextInput(attrs = {"class": "input-small"}),
            "weld_material_1": forms.Select(attrs = {"class": "input-small"}),
            "weld_material_2": forms.Select(attrs = {"class": "input-small"}),
            "weld_method": forms.Select(attrs = {"class": "input-small"}),
            "weldseam_type": forms.Select(attrs = {"class": "input-small"}),
            "size_1": forms.TextInput(attrs = {"class": "input-small"}),
            "size_2": forms.TextInput(attrs = {"class": "input-small"}),
            "remark": forms.TextInput(attrs = {"class": "input-medium"}),
            "groove_inspction": forms.SelectMultiple(attrs = {"class": "input-small"}),
            "welded_status_inspection": forms.SelectMultiple(attrs = {"class": "input-small"}),
            "heat_treatment_inspection": forms.SelectMultiple(attrs = {"class": "input-small"}),
            "pressure_test_inspection": forms.SelectMultiple(attrs = {"class": "input-small"}),
        }

class WeldJointTechDetailForm(forms.ModelForm):
    """
    mxl
    """
    class Meta:
        model = WeldJointTechDetail
        exclude = ('id', 'weld_joint')
        widgets = {
            "joint_index" : forms.TextInput(attrs = {"class" : "input-small"}),
            "bm_texture_1" : forms.TextInput(attrs = {"class" : "input-small", "readonly" : "true"}),
            "bm_texture_2" : forms.TextInput(attrs = {"class" : "input-small", "readonly" : "true"}),
            "bm_specification_1" : forms.TextInput(attrs = {"class" : "input-small", "readonly" : "true"}),
            "bm_specification_2" : forms.TextInput(attrs = {"class" : "input-small", "readonly" : "true"}),
            "weld_method" : forms.TextInput(attrs = {"class" : "input-small", "readonly" : "true"}),
            "procedureQualification_index" : forms.Select(attrs = {"class" : "input-small"}),
            "weld_certification" : forms.SelectMultiple(attrs = {"class" : "input-xlarge"}),
            "remark" : forms.TextInput(attrs = {"class" : "input-xxlarge"}),
        }

class ProcessingRouteForm(forms.ModelForm):
    """
    JunHU
    """
    class Meta:
        model = Processing
        exclude = ('materiel_belong', 'GS1', 'GS2', 'GS3', 'GS4', 
                  'GS5', 'GS6', 'GS7', 'GS8', 'GS9', 'GS10', 
                  'GS11', 'GS12') 
        widgets = {
            "GX1" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "GX2" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "GX3" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "GX4" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "GX5" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "GX6" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "GX7" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "GX8" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "GX9" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "GX10" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "GX11" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "GX12" : forms.Select(attrs = {"class" : "form-control input-mini"}),
        }
    def clean(self):
        cleaned_data = super(ProcessingRouteForm, self).clean()
        for i in range(2, 13):
            curfield = "GX%d" % i
            prevfield = "GX%d" % (i - 1)
            if cleaned_data.get(curfield) != None and cleaned_data.get(prevfield) == None:
                raise forms.ValidationError("工序路线必须连续")
        return cleaned_data

class ProcessInfoForm(forms.ModelForm):
    """
    JunHU
    """
    class Meta:
        model = Processing
        exclude = ("materiel_belong", "name", "next_processing", "is_first_processing", )
        widgets = {
            "instruction" : forms.TextInput(attrs = {"class" : "input-small"}),
            "index" : forms.TextInput(attrs = {"class" : "input-small"}),
            "hour" : forms.TextInput(attrs = {"class" : "input-small"}),
        }
class CirculationRouteForm(forms.ModelForm):
    """
    mxl
    """
    class Meta:
        model = CirculationRoute
        exclude = ('materiel_belong')
        widgets = {
            "L1" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L2" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L3" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L4" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L5" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L6" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L7" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L8" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L9" : forms.Select(attrs = {"class" : "form-control input-mini"}),
            "L10" : forms.Select(attrs = {"class" : "form-control input-mini"}),
        }
    #def __init__(self, *args, **kwargs):
    #    super(CirculationRouteForm, self).__init__(*args, **kwargs)
    #    for field in self.fields:
    #        self.fields[field] = forms.ChoiceField(widget = forms.Select(attrs = {'class' : 'form-control input-mini',}))
    def clean(self):
        cleaned_data = super(CirculationRouteForm, self).clean()
        for i in range(2, 11):
            curfield = "L%d" % i
            prevfield = "L%d" % (i - 1)
            #print cleaned_data.get(prevfield)
            #print cleaned_data.get(curfield)
            if cleaned_data.get(curfield) != None and cleaned_data.get(prevfield) == None:
                #print "circulation error"
                raise forms.ValidationError("流转路线必须连续")
        return cleaned_data

class TransferCardForm(forms.Form):
    """
    JunHU
    """
    card_type = forms.ChoiceField(choices = TRANSFER_CARD_TYPE_CHOICES, widget = forms.Select(attrs = {'class': 'input'}))

class CategoriesForm(forms.Form):
    """
    MH Chen
    """
    categorie_type = forms.ChoiceField(choices = MATERIAL_CATEGORY_CHOICES, widget = forms.Select(attrs = {'class': 'input',"disabled":'disabled'}))

class ProgramFeedbackForm(forms.Form):
    """
    JunHU
    """
    need_correct = forms.BooleanField(required = False, widget = forms.CheckboxInput())
    feedback = forms.CharField(required = True, widget = forms.Textarea(attrs = {"rows": "5", "cols": "50"}))

class AuxiliaryMaterielForm(forms.ModelForm):
    """
    MH Chen
    """
    class Meta:
        model = Materiel
        exclude = ("id", "order","parent_schematic_index")
        widgets = {
            "name": forms.TextInput(attrs = {"class": "input-medium","readonly":'readonly'}),
            "index": forms.TextInput(attrs = {"class": "input-small","readonly":'readonly'}),
            "schematic_index": forms.TextInput(attrs = {"class": "input-medium","readonly":'readonly'}),
            "material": forms.Select(attrs = {"class": "input-medium","disabled":'disabled'}),
            "count": forms.TextInput(attrs = {"class": "input-medium","readonly":'readonly'}),
            "remark": forms.TextInput(attrs = {"class": "input-medium","readonly":'readonly'}),
            "net_weight": forms.TextInput(attrs = {"class": "input-medium","readonly":'readonly'}),
            "total_weight": forms.TextInput(attrs = {"class": "input-medium","readonly":'readonly'}),
            "specification": forms.TextInput(attrs = {"class": "input-medium","readonly":'readonly'}),
            "quota_coefficient": forms.TextInput(attrs = {"class": "input-medium"}),
            "quota": forms.TextInput(attrs = {"class": "input-medium"}),
            
        }

class TechPreparationPlanForm(forms.ModelForm):
    """
    mxl
    """
    class Meta:
        model = TechPlan
        fields = ("detail", "sentDepartment", "planCompleteDate")
        widgets = {
            "planCompleteDate" : forms.TextInput(attrs = {'class' : 'form-control', 'id' : 'date'})
        }

class UploadForm(forms.Form):
    """
    BinWu
    """
    pic = forms.FileField(label="导入图片", required=False,
                         widget=forms.FileInput())
