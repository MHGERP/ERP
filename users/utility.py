#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-07-26 11:34
# Last modified: 2016-07-26 11:39
# Filename: utility.py
# Description:
from django.contrib.auth.models import User
from users.models import UserInfo

def createNewUser(username, password, fullname = None):
    try:
        user = User.objects.create_user(username = username, password = password)
        user.save()

        userinfo = UserInfo(user = user, name = fullname)
        userinfo.save()
    except IntegrityError, e:
        raise e

def getUserByAuthority(authority):
    #auth_obj = Authority.objects.get(authority = authority)
    #user_list = User.objects.filter(title_user__authorities = auth_obj).distinct()
    #return user_list    
    return None
