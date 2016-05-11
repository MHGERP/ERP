#!/usr/bin/env python
# coding=utf-8
from django.contrib import admin
from sell.models  import *

RegisterClass = (
    Product,
    BidFile,
)

for item in RegisterClass:
    admin.site.register(item)
