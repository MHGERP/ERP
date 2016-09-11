#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-07-26 11:48
# Last modified: 2016-07-26 11:50
# Filename: views.py
# Description:
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.template import RequestContext

#from users.decorators import checkSuperAdmin

def loginviews(request):
    return render(request,"login.html")

def login_redirect(request):
    try:
        del request.session["is_super_admin"]
    except:
        pass

    #request.session["is_super_admin"] = checkSuperAdmin(request.user)

    redirect_url = "/home"
    return HttpResponseRedirect(redirect_url)

def logout_redirect(request):
    try:
        del request.session["is_super_admin"]
    except:
        pass

    return HttpResponseRedirect('/')
