#!/usr/bin/env python
# coding=utf-8 
from const import *

def entryConfirm(entry_obj,person,role):
    setattr(entry_obj,role,person)
    entry_obj.save()

def getEntrySet(model_type,status):
    return model_type.objects.filter(entry_status = status)
