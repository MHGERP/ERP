#!/usr/bin/env python
# coding=utf-8 
from const import *
from users.models import Title,Authority
from django.contrib.auth.models import User

def getUserByAuthority(authority):
    auth_obj = Authority.objects.get(authority = authority)
    user_list = User.objects.filter(title_user__authorities = auth_obj)
    return user_list    

