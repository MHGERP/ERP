#coding: UTF-8

from const import *
from django.db import models
from django.contrib.auth.models import User

class SuperAdmin(models.Model):
    admin = models.ForeignKey(User, blank = False, verbose_name = u"管理员")
    class Meta:
        verbose_name = u"超级管理员"
        verbose_name_plural = u"超级管理员"
    def __unicode__(self):
        return self.admin.user_name

class Group(models.Model):
    admin = models.ForeignKey(User, blank = True, null = True, verbose_name = u"群组管理员")
    name = models.CharField(max_length = 100, blank = False, verbose_name = u"群组名")
    class Meta:
        verbose_name = u"群组"
        verbose_name_plural = u"群组"
    def __unicode__(self):
        return self.name

class Authority(models.Model):
    authority = models.CharField(max_length = 100, blank = False, choices = AUTHORITY_SET, verbose_name = u"权限名")
    class Meta:
        verbose_name = u"页面权限"
        verbose_name_plural = u"页面权限"
    def __unicode__(self):
        return self.get_authority_display()

class Title(models.Model):
    group = models.ForeignKey(Group, blank = False, verbose_name = u"所属群组")
    name = models.CharField(max_length = 100, blank = False, verbose_name = u"头衔名")
    users = models.ManyToManyField(User, blank = True, null = True, verbose_name = u"拥有头衔用户")
    authorities = models.ManyToManyField(Authority, blank = True, null = True, verbose_name = u"拥有权限")
    class Meta:
        verbose_name = u"头衔"
        verbose_name_plural = u"头衔"
    def __unicode__(self):
        return self.name
