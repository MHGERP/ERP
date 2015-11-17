# coding: UTF-8
from django.shortcuts import render, redirect
from const.forms import InventoryTypeForm
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
import json
from django.db import transaction
from django.contrib.auth.models import User
from backend.utility import getContext


def techPreparationPlanViews(request):
    context = {}
    return render(request, "techdata/tech_preparation_plan.html", context)

def processExaminationViews(request):
    context = {}
    return render(request, "techdata/process_examinationViews.html", context)