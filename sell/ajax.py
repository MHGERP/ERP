#!/usr/bin/env python
# coding=utf-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.utils import simplejson

from django.db.models import Q
from django.contrib.auth.models import User

from const import *
from backend.utility import getContext

@dajaxice_register
def getProductionList(request):
   productions = []
   return render_to_string("sell/widgets/productions_table.html")
