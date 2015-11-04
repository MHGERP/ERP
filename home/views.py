# coding: UTF-8
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators import csrf

def homepageViews(request):
    context = {}
    return render(request,"home/homepage.html",context)
