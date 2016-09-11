#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-07-26 10:47
# Last modified: 2016-09-11 13:15
# Filename: models.py
# Description:

from const import *
from users import *

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as _Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class UserInfo(models.Model):
    user = models.OneToOneField(User, verbose_name=u"用户")
    name = models.CharField(blank=True, null=True,
                            max_length=20, verbose_name=u"姓名")
    phone = models.CharField(blank=True, null=True,
                             max_length=20, verbose_name=u"电话")
    mobile = models.CharField(blank=True, null=True,
                              max_length=20, verbose_name=u"移动电话")
    sex = models.IntegerField(blank=True, null=True,
                              choices=SEX_CHOICES, verbose_name=u"性别")
    role = models.ForeignKey('Role', blank=True, null=True,
                                verbose_name=u'头衔')

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = u"用户信息"

    def __unicode__(self):
        return self.name


class Group(models.Model):
    admin = models.ForeignKey(User, blank=True, null=True,
                              verbose_name=u"部门管理员", related_name='admin')
    name = models.CharField(max_length=100, blank=False,
                            verbose_name=u"部门名")
    cate = models.CharField(max_length=100, blank=False,
                            verbose_name=u'简写')

    class Meta:
        verbose_name = u"部门"
        verbose_name_plural = u"部门"

    def __unicode__(self):
        return self.name


class Role(_Group):
    group = models.ForeignKey(Group, blank=False, null=False,
                              related_name='roles')
    title = models.CharField(max_length=100, blank=False, null=False,
                             verbose_name=u'头衔')

    class Meta:
        verbose_name = u'角色'
        verbose_name_plural = u'角色'

    def __unicode__(self):
        return self.group.name+'|'+self.title


class GlobalPermissionManager(models.Manager):
    def get_query_set(self):
        return super(GlobalPermissionManager, self).get_query_set().\
            filter(content_type__name='global_permission')


class GlobalPermission(Permission):
    """ A global permission object should not attached to any model. """
    objects = GlobalPermissionManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        ct, created = ContentType.objects.get_or_create(
            name='global_permission',
            #app_label=self._meta.app_label)
            #app_label='global')
            app_label=kwargs['category'])
        self.content_type = ct
        super(GlobalPermission, self).save(*args, **kwargs)
