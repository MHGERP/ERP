from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.db.models import Q
from users.models import *
from django.contrib.auth.models import User

@dajaxice_register
def searchUser(request,search_user):
    if search_user!="":
        user_list = User.objects.filter(Q(username__icontains=search_user) | Q(userinfo__name__icontains=search_user))
        #user_list = User.objects.filter(username__icontains=search_user)
    else:
        user_list = User.objects.all()
    

    context = {
            "user_list": user_list,
       }
    html = render_to_string("management/widgets/user_table.html", context)
    return html

    
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
def createOrModifyGroup(request, name, group_id):
    """
    JunHU
    summary: ajax function to create or modify a group
    params: name: new group name str or "-1"
    return: NULL
    """
    if group_id != "-1":
        group = Group.objects.get(id = group_id)
        group.name = name
        group.save()
    else:
        new_group = Group(name = name)
        new_group.save()

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

@dajaxice_register
def getTitleList(request, group_id):
    """
    JunHU
    summary: ajax function to get all title belong to one group
    params: group_id: db id of group
    return: title list html string
    """
    title_list = Title.objects.filter(group = group_id)
    context = {
        "title_list": title_list,
    }
    html = render_to_string("management/widgets/title_table.html", context)
    return html

@dajaxice_register
def createUser(request, user_name, user_password):
    try:
        user=User(username=user_name,password=user_password)
        user.save()
    except Exception,e:
        return "fail"



@dajaxice_register
def createOrModifyTitle(request, group_id, title_name, title_id):
    """
    JunHU
    summary: ajax function to create or modify a title
    params: name: new group name str or "-1"
    return: NULL

    """
    if title_id == "-1":
        group = Group.objects.get(id = group_id)
        new_title = Title(group = group, name = title_name)
        new_title.save()
    else:
        title = Title.objects.get(id = title_id)
        title.name = title_name
        title.save()

@dajaxice_register
def deleteTitle(request, title_id):
    """
    JunHU
    summary: ajax function to delete a exist title
    params: id: db id of title
    return: NULL
    """
    title = Title.objects.get(id = title_id)
    title.delete()

@dajaxice_register
def getAuthList(request, auth_type, title_id):
    """
    JunHU
    summary: ajax function to get the author list
    params: auth_type: the type of request auth; title_id: db id of title
    return: auth list html string
    """
    auth_list = Authority.objects.filter(auth_type = auth_type)
    title = Title.objects.get(id = title_id)
    for auth in auth_list:
        auth.checked = (auth in title.authorities.all())
    context = {
        "auth_list": auth_list,
    }
    html = render_to_string("management/widgets/auth_table.html", context)
    return html

@dajaxice_register
def addOrRemoveAuth(request, auth_id, title_id, flag):
    """
    JunHU
    summary: ajax function to add or remove connection between one auth and one title
    params: auth_id: db id of auth; title_id: db id of title; flag: indicate add or remove
    return: result info
    """
    try:
        auth = Authority.objects.get(id = auth_id)
        title = Title.objects.get(id = title_id)
        if flag:
            title.authorities.add(auth)
        else:
            title.authorities.remove(auth)
        return "ok"
    except:
        return "fail"
