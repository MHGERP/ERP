# coding: UTF-8
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
import json, datetime, xlrd
from django.db import transaction
from django.contrib.auth.models import User
from backend.utility import getContext

def productionsView(request):
    context = {

    }
    return render(request, "sell/productions.html", context)
