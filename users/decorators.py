#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-09-11 09:22
# Last modified: 2016-09-11 12:19
# Filename: decorators.py
# Description:

import os
import sys
import datetime
import functools

from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators import csrf
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from users.models import *


def permission_required(perm, login_url=None, raise_exception=False):
    def check_perms(user):
        # First check if the user has the permission (even anon users)
        if user.has_perm(perm):
            return True
        # Second check if the role has the permission
        if isinstance(user, AnonymousUser):
            return False
        if user.userinfo.role is not None and perm in set(
                [u'%s.%s' % (p.content_type.app_label, p.codename)
                 for p in user.userinfo.role.permissions.all()]):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)

def permission_check(func):
    @functools.wraps(func)
    def func_wrapper(request, *args, **kwargs):
        def check_perms(user, perm):
            # First check if the user has the permission (even anon users)
            if user.has_perm(perm):
                return True
            # Second check if the role has the permission
            if user.userinfo.role is not None and perm in set(
                    [u'%s.%s' % (p.content_type.app_label, p.codename)
                     for p in user.userinfo.role.permissions.all()]):
                return True
            # In case the 403 handler should be called raise the exception
            raise PermissionDenied
            # As the last resort, show the login form
            return False
        try:
            module = ''.join(str(func.__module__).rsplit('.ajax', 1))
            name = '.'.join((module, func.__name__))
            if check_perms(request.user, name):
                return func(request, *args, **kwargs)
        except PermissionDenied:
            raise PermissionDenied
        return False
    return func_wrapper
