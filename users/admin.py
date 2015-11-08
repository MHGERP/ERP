#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from users.models  import Title, Group, Authority, SuperAdmin, UserInfo

RegisterClass = (
    Title,
    Group,
    Authority,
    SuperAdmin,
    UserInfo,
)

for item in RegisterClass:
    admin.site.register(item)
