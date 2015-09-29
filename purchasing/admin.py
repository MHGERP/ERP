#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from purchasing.models  import *

RegisterClass = (
    BidForm,
    ArrivalInspection,
)

for item in RegisterClass:
    admin.site.register(item)
