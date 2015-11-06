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


from forms import GroupForm
from users.models import Title

def userManagementViews(request):
    """
    JunHU
    """
    context = {}
    return render(request, "management/user_management.html", context)

def groupManagementViews(request):
    """
    JunHU
    """
    context = {}
    return render(request, "management/group_management.html", context)

def titleManagementViews(request):
    """
    JunHU
    """
    form = GroupForm()
    context = {
            "form": form,
        }
    return render(request, "management/title_management.html", context)

def messageManagementViews(request):
    """
    JunHU
    """
    context = {}
    return render(request, "management/message_management.html", context)

def authorityManagementViews(request):
    """
    JunHU
    """
    title_id = request.GET.get("title_id")
    title = Title.objects.get(id = title_id)
    context = {
            "title": title,
        }
    return render(request, "management/authority_management.html", context)
