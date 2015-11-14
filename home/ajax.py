from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.models import User
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from users.models import *
from backend.utility import getContext
from users.utility import createNewUser
from backend.utility import getContext
from form import userInfoForm

@dajaxice_register
def updateUserInfo(request,user_form):
	user_form=userInfoForm(deserialize_form(user_form),instance=request.user.userinfo)
	if user_form.is_valid():
		user_form.save()
		log="save success"
	else:
		log="form error"
	print user_form.errors
	return log

@dajaxice_register
def getUserInfoForm(request):
	user_form = userInfoForm(instance=request.user.userinfo)
	userinfoform=render_to_string("base/userinfoform.html",{"user_form":user_form})
	return userinfoform

  
