#!/usr/bin/env python
# coding=utf-8 
from const import *
from users.models import Title,Authority
from django.contrib.auth.models import User
from const.models import Material
from django.db.models import Q
from techdata.models import Processing

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

def checkAuthority(authority,user):
    """
    author: shenlian
    func: check authority
    """
    return getUserByAuthority(authority).filter(id = user.id).count() > 0 

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

def getDistinctSet(_Model,_FModel,field):
    obj_list = _Model.objects.values(field).distinct()
    obj_set = []
    for obj_tmp in obj_list:
        if obj_tmp[field] != None:
            obj_set.append(_FModel.objects.get(id = obj_tmp[field]))
    return  obj_set
def getMaterialQuerySet(*categories):
    """
    JunHU
    """
    qset = reduce(lambda x, y: x | y, [Q(categories = cate) for cate in categories]) 
    return Material.objects.filter(qset)

def getProcessList(item):
    """
    JunHU
    summary: get all process of one materiel
    params: materiel item
    return: process list
    """
    try:
        process = Processing.objects.get(materiel_belong = item, is_first_processing = True)  
        process_list = []
        while process:
            process_list.append(process)
            process = process.next_processing
    except:
        process_list = []
    return process_list

