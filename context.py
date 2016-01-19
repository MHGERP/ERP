# coding: UTF-8
"""
    Author:tianwei
    Email: liutianweidlut@gmail.com
    Desc: settings context processor for templates,
          then we can use
"""

from django.conf import settings
#from backend.decorators import check_auth
#from backend.logging import loginfo 
#from backend.logging import loginfo
from const import *

all_required = ()


def application_settings(request):
    """The context processor function"""
    mysettings={}
    for keyword in all_required:
        mysettings[keyword] = getattr(settings, keyword)

    context = {
        'settings': mysettings,
    }
    return context

def userauth_settings(request):
    #"""
    #The context processor will add user authorities variables
    #into all template
    #"""
    print request.path
    context={}
    return context
    #userauth = {
                #"is_adminstaff": False,
                #"is_schooler": False,
                #"is_colleger":False,
                #"is_experter": False,
                #"is_teacher": False,
                #"is_finance":False,
                #}
    #auth_choices= {
        #"adminStaff":ADMINSTAFF_USER,
        #"school":SCHOOL_USER,
        #"college":COLLEGE_USER,
        #"teacher":TEACHER_USER,
        #"expert":EXPERT_USER,
        #"finance":FINANCE_USER,
    #}
    #identity = request.session.get('auth_role', "")
    #if identity == ADMINSTAFF_USER and check_auth(user=request.user, authority=ADMINSTAFF_USER):
        #userauth["is_adminstaff"] = True
        #try:
            #userauth["adminstaff"] = AdminStaffProfile.objects.get(userid=request.user)
        #except AdminStaffProfile.DoesNotExist, err:
            #loginfo(p=err, label="context AdminStaffProfile")
    #if identity == FINANCE_USER and check_auth(user=request.user, authority=FINANCE_USER):
        #userauth["is_finance"] = True
        #try:
            #userauth["finance"] = FinanceProfile.objects.get(userid=request.user)
        #except FinanceProfile.DoesNotExist, err:
            #loginfo(p=err, label="context FinanceProfile")

    #if identity == SCHOOL_USER and check_auth(user=request.user, authority=SCHOOL_USER):
        #userauth["is_schooler"] = True
        #try:
            #userauth["school"] = SchoolProfile.objects.get(userid=request.user)
        #except SchoolProfile.DoesNotExist, err:
            #loginfo(p=err, label="context SchoolProfile")
    #if identity == COLLEGE_USER and check_auth(user=request.user, authority=COLLEGE_USER):
        #userauth["is_colleger"] = True
        #try:
            #userauth["college"] = CollegeProfile.objects.get(userid=request.user)
        #except CollegeProfile.DoesNotExist, err:
            #loginfo(p=err, label="context CollegeProfile")

    #if identity == EXPERT_USER and check_auth(user=request.user, authority=EXPERT_USER):
        #userauth["is_experter"] = True
        #try:
            #userauth["expert"] = ExpertProfile.objects.get(userid=request.user)
        #except ExpertProfile.DoesNotExist, err:
            #loginfo(p=err, label="context ExpertProfile")

    #if identity == TEACHER_USER and check_auth(user=request.user, authority=TEACHER_USER):
        #userauth["is_teacher"] = True
        #try:
            #userauth["teacher"] = TeacherProfile.objects.get(userid=request.user)
        #except TeacherProfile.DoesNotExist, err:
            #loginfo(p=err, label="context TeacherProfile")
    #context = {"userauth": userauth,
               #"auth_choices":auth_choices,
    #}
    #return context

