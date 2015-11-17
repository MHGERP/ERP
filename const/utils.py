#!/usr/bin/env python
# coding=utf-8 
from const import *
from users.models import Title,Authority
from django.contrib.auth.models import User

def getUserByAuthority(authority):
    """
    author: Shen Lian
    func:   get user_set by authority
    params: authority: user's authority
    return: user_list
    """
    auth_obj = Authority.objects.get(authority = authority)
    user_list = User.objects.filter(title_user__authorities = auth_obj)
    return user_list    

def getChoiceList(obj_set,field):
    """
    author: Shen Lian
    func:   get form choice through model set
    params: obj_set:model set; field:model field
    return: model tuple 
    """
    obj_list = [(-1,"------")]
    for obj in obj_set:
        obj_list.append((obj.id,getattr(obj,field)))
    return tuple(obj_list)
