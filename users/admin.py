#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from users.models  import *

RegisterClass = (
    Title,
    Group,
    Authority,
    SuperAdmin,

)

for item in RegisterClass:
    admin.site.register(item)
