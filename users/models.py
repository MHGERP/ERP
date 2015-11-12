#coding: UTF-8

from const import *
from users import *

from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, verbose_name = u"用户")
    name = models.CharField(blank = True, null = True, max_length = 20, verbose_name = u"姓名")
    phone = models.CharField(blank = True, null = True, max_length = 20, verbose_name = u"电话")
    mobile = models.CharField(blank = True, null = True, max_length = 20, verbose_name = u"移动电话")
    sex = models.IntegerField(blank = True, null = True, choices = SEX_CHOICES, verbose_name = u"性别")
    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = u"用户信息"
    def __unicode__(self):
        return self.name

class SuperAdmin(models.Model):
    admin = models.ForeignKey(User, blank = False, verbose_name = u"管理员")
    class Meta:
        verbose_name = u"超级管理员"
        verbose_name_plural = u"超级管理员"
    def __unicode__(self):
        return self.admin.user_name

class Group(models.Model):
    admin = models.ForeignKey(User, blank = True, null = True, verbose_name = u"部门管理员")
    name = models.CharField(max_length = 100, blank = False, verbose_name = u"部门名")
    class Meta:
        verbose_name = u"部门"
        verbose_name_plural = u"部门"
    def __unicode__(self):
        return self.name

class Authority(models.Model):
    auth_type = models.IntegerField(blank = False, choices = AUTH_TYPE_CHOICES, verbose_name = u"权限类型")
    authority = models.CharField(max_length = 100, blank = False, choices = AUTHORITY_SET, verbose_name = u"权限名")
    class Meta:
        verbose_name = u"页面权限"
        verbose_name_plural = u"页面权限"
    def __unicode__(self):
        return self.get_authority_display()

class Title(models.Model):
    group = models.ForeignKey(Group, blank = False, verbose_name = u"所属部门")
    name = models.CharField(max_length = 100, blank = False, verbose_name = u"头衔名")
    users = models.ManyToManyField(User, blank = True, null = True, verbose_name = u"拥有头衔用户",related_name="title_user")
    authorities = models.ManyToManyField(Authority, blank = True, null = True, verbose_name = u"拥有权限")
    class Meta:
        verbose_name = u"头衔"
        verbose_name_plural = u"头衔"
    def __unicode__(self):
        return self.group.name + self.name
