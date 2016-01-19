#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from production.models  import *

RegisterClass = (
    SynthesizeFileListStatus,
)
for item in RegisterClass:
    admin.site.register(item)