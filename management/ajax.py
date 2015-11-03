from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string

from users.models import *
from django.contrib.auth.models import User

@dajaxice_register
def getGroupList(request):
    """
    JunHU
    summary: ajax function to get all group info
    params: NULL
    return: group list html string
    """
    group_list = Group.objects.all()
    context = {
            "group_list": group_list,
       }
    html = render_to_string("management/widgets/group_table.html", context)
    return html

@dajaxice_register
def addNewGroup(request, name):
    """
    JunHU
    summary: ajax function to add a new group
    params: name: new group name str
    return: result info
    """
    try:
        new_group = Group(name = name)
        new_group.save()
        return "ok"
    except:
        return "fail"

@dajaxice_register
def deleteGroup(request, id):
    """
    JunHU
    summary: ajax function to delete a exist group
    params: id: db id of group
    return: result info
    """
    try:
        group = Group.objects.get(id = id)
        group.delete()
        return "ok"
    except:
        return "fail"
  
@dajaxice_register
def searchCandidate(request, key):
    """
    JunHU
    summary: ajax function to get candidate list
    params: key: keyword about candidate
    return: candidate list html string
    """
    candidate_list = User.objects.filter(username__icontains = key)
    context = {
        "candidate_list": candidate_list,
    }
    html = render_to_string("management/widgets/candidate_table.html", context)
    return html

@dajaxice_register
def addAdmin(request, group_id, user_id):
    """
    JunHU
    summary: ajax function to add new group admin
    params: group_id: db id of group; user_id: db id of user
    return: result info
    """
    try:
        group = Group.objects.get(id = group_id)
        user = User.objects.get(id = user_id)
        group.admin = user
        group.save()
        return "ok"
    except:
        return "fail"
