# coding: UTF-8
from django.shortcuts import render
from const.forms import InventoryTypeForm
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
import json
from django.db import transaction


def userManagementViews(request):
    """
    JunHU
    """
    context = {}
    return render(request, "management/user_management.html", context)

