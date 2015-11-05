#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from news.models  import *

RegisterClass = (
    NewsCategory,
    News,
    DocumentFile,
)

for item in RegisterClass:
    admin.site.register(item)