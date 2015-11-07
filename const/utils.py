#!/usr/bin/env python
# coding=utf-8 

def entryConfirm(entry_obj,person,role):
    setattr(entry_obj,role,person)
    entry_obj.save()

def getEntrySet(model_type,role):
    role_list = ["purchase","keeper","inspector"]
    role_dic = {}
    #for role_tmp in role_list:
    #if role_tmp == role:
    #        role_dic[role_tmp + "__isnull"] = False
    #    else:
    #        role_dic[role_tmp + "__isnull"] = True
    role_dic[role + "__isnull"] = True
    return model_type.objects.filter(**role_dic)
