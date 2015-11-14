# coding: UTF-8

import os
import sys
import datetime

from django.contrib.auth.models import User
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
from django.contrib.auth.decorators import login_required

from users.models import *
from backend.logging import loginfo

def check_auth(user = None, authority = None):
    """
    JunHU
    summary: function to check one user has one authority
    params: user: user object, authority: auth string of authority
    return: boolean value
    """
    if user is None or authority is None or user.is_anonymous() is True:
        return False
    try:
        auth = Authority.objects.get(authority = authority)
    except Authority.DoesNotExist, err:
        loginfo(p=err, label="ERROR in check_auth function!!!")
        return False
    if user.title_user and user.title_user.filter(authorities = auth).count() > 0:
        return True

    return False

class authority_required(object):
    """
    JunHU
    summary: functor of authority decorator
    params: authority: authority alias
    return: wrappered functor
    """
    def __init__(self, authority):
        self.authority = authority

    def __call__(self, method):
        def wrappered_method(request, *args, **kwargs):
            user = request.user
            is_passed = check_auth(user = request.user, authority = self.authority)
            if is_passed:
                response = method(request, *args, **kwargs)
                return response
            else:
                return HttpResponseRedirect(reverse('backend.errorviews.error403'))
        return wrappered_method
