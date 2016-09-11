#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-07-26 11:38
# Last modified: 2016-09-11 09:03
# Filename: admin.py
# Description:
#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from .models import *

RegisterClass = (
        Group,
        Role,
        UserInfo,
)

for item in RegisterClass:
    admin.site.register(item)
