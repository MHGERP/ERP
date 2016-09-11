#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-09-11 09:50
# Last modified: 2016-09-11 12:19
# Filename: views.py
# Description:
# Create your views here.
from .models import *

def is_group_admin(group, user):
    if group is not None and user is not None and group.admin is user:
        return True
    else:
        return false
