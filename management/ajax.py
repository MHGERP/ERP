#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-09-11 08:08
# Last modified: 2016-09-11 13:28
# Filename: ajax.py
# Description:
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.utils import simplejson

from django.db.models import Q
from users.models import *
from news.models import *
from users.views import *
from django.contrib.auth.models import User

from backend.utility import getContext
from users.utility import createNewUser


@dajaxice_register
def searchUser(request, search_user, page):
    page = int(page)
    if request.user.is_superuser:
        user_list = User.objects.all()
    elif is_group_admin(request.user.user.role.group, request.user):
        user_list = User.objects.all()
    else:
        user_list = []

    if search_user != "":
        user_list = user_list.filter(Q(username__icontains=search_user) | Q(userinfo__name__icontains=search_user))
    context = getContext(user_list, page, "item", 0)
    for user in context["item_list"]:
        if hasattr(user, 'userinfo') and user.userinfo.role is not None:
            user.titles = unicode(user.userinfo.role)
        else:
            user.titles = u'无'
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
    context = {"group_list": group_list}
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
        group = Group.objects.get(id=group_id)
        group.name = name
        group.save()
    else:
        new_group = Group(name=name)
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
        group = Group.objects.get(id=id)
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
    candidate_list = User.objects.filter(Q(username__icontains=key) | Q(userinfo__name__icontains=key))
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
        group = Group.objects.get(id=group_id)
        user = User.objects.get(id=user_id)
        group.admin = user
        group.save()
        return "ok"
    except:
        return "fail"


@dajaxice_register
def getTitleList(request, group_id, setting_user=False):
    """
    JunHU
    edited:David
    summary: ajax function to get all title belong to one group
    params: group_id: db id of group
    return: title list html string
    """
    title_list = Role.objects.filter(group=group_id)
    if setting_user:
        user = User.objects.get(id=setting_user)
        for title in title_list:
            title.checked = (user in map(lambda x: x.user, title.userinfo_set.all()))
    context = {
        "title_list": title_list,
    }

    html = setting_user and \
        render_to_string("management/widgets/title_setting_table.html", context) or \
        render_to_string("management/widgets/title_table.html", context)
    return html


@dajaxice_register
def getMessageList(request, loguser):
    """
    BinWu
    summary: ajax function to get all message writen by loguser
    params: loguser: db id of the user who logs in
    return: message list  html string
    """
    message_list = Message.objects.filter(writer=loguser)
    context = {
        "message_list": message_list,
    }
    html = render_to_string("management/widgets/message_table.html", context)
    return html


@dajaxice_register
def getBoxList(request):
    """
    BinWu
    """
    print ("I am here")
    box_list = MessageBox.objects.filter(user__id=request.user.id).order_by("read", "message")
    context = {
        "box_list": box_list,
    }
    html = render_to_string("management/modal-message.html", context)
    return html


@dajaxice_register
def deleteMessage(request, messageId):
    """
    BinWu
    summary: ajax function to delete the message which is revoked by the writer
    params: message: db id of the message needs to be revoked
    return: "success"
    """
    print ("This is messageId")
    print (messageId)
    messageObject = Message.objects.get(id=messageId)
    print ("before delete")
    messageObject.delete()
    return "success"


@dajaxice_register
def checkMessage(request, messageId):
    """
    BinWu
    summary: ajax function to check the content of the message
    paras: message: db id of the message for checking
    return: "data"
    """
    messageObject = Message.objects.get(id=messageId)
    file = DocumentFile.objects.filter(message=messageId)
    file_name = []
    file_list = []
    for f in file:
        file_name.append(f.news_document.name[26:])
        file_list.append(f.news_document.path)
    data = {
        "message_title": messageObject.title,
        "message_content": messageObject.content,
        "filepath": file_list,
        "filename": file_name,
    }
    print("title")
    print(data['message_title'])
    print(file_list)
    return simplejson.dumps(data)


@dajaxice_register
def checkBox(request, boxId):
    """
    BinWu
    summary: ajax function to check the content of the messagebox
    paras: message: db id of the message for checking
    return: "data"
    """
    boxObject = MessageBox.objects.get(id=boxId)
    messageId = boxObject.message.id
    boxObject.read = True
    boxObject.save()
    messageObject = Message.objects.get(id=messageId)
    file = DocumentFile.objects.filter(message=messageId)
    file_name = []
    file_list = []
    for f in file:
        file_name.append(f.news_document.name[26:])
        file_list.append(f.news_document.path)
    data = {
        "message_title": messageObject.title,
        "message_content": messageObject.content,
        "filepath": file_list,
        "filename": file_name,
    }
    print("title")
    print(data['message_title'])
    print(file_list)
    return simplejson.dumps(data)


@dajaxice_register
def createUser(request, user_name, user_password, user_fullname):
    try:
        createNewUser(username=user_name, password=user_password, fullname=user_fullname)
    except:
        return "fail"


@dajaxice_register
def createOrModifyTitle(request, group_id, role_name, role_id):
    """
    JunHU
    edited:David
    summary: ajax function to create or modify a title
    params: name: new group name str or "-1"
    return: NULL

    """
    if role_id == "-1":
        group = Group.objects.get(id=group_id)
        new_role = Role(group=group, title=role_name, name=group.name+role_name)
        new_role.save()
    else:
        role = Role.objects.get(id=role_id)
        role.title = role_name
        role.name = role.group.name+role_name
        role.save()


@dajaxice_register
def deleteTitle(request, role_id):
    """
    JunHU
    edited:David
    summary: ajax function to delete a exist title
    params: id: db id of title
    return: NULL
    """
    role = Role.objects.get(id=role_id)
    related_users = User.objects.filter(userinfo__role=role)
    for user in related_users:
        user.userinfo.role = None
        user.userinfo.save()
    role.delete()


@dajaxice_register
def deleteUser(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()


@dajaxice_register
def getNewsList(request, news_cate, page=1):
    """
    mxl
    """
    try:
        page = int(page)
    except:
        page = 1
    news_list = News.objects.filter(news_category__category=news_cate).order_by('-news_date')
    context = getContext(news_list, page, "item", 0)
    html = render_to_string("management/widgets/news_table.html", context)
    # return html
    return simplejson.dumps({'html': html})


@dajaxice_register
def deleteNews(request, news_id):
    """1,cfnsv
    mxl
    """
    news = News.objects.get(id=news_id)
    news.delete()


@dajaxice_register
def getControlList(request, auth_type, role_id):
    """
    JunHU
    edited:David
    summary: ajax function to get the author list
    params: auth_type: the type of request auth; title_id: db id of title
    return: auth list html string
    """
    auth_list = filter(lambda x: x.content_type.app_label == auth_type, GlobalPermission.objects.all())
    role = Role.objects.get(id=role_id)
    role_perms = set([u'%s.%s' % (p.content_type.app_label, p.codename) for p in role.permissions.all()])
    for auth in auth_list:
        auth.cate, auth.name = auth.name.split('|')
        if auth_type+'.'+auth.codename in role_perms:
            auth.checked = True
        else:
            auth.checked = False
    context = {
        "auth_list": auth_list,
    }
    html = render_to_string("management/widgets/control_table.html", context)
    return html


@dajaxice_register
def addOrRemoveTitle(request, role_id, user_id, flag):
    """
    JunHU
    edited:David
    summary: ajax function to add or remove connection between one user and one title
    params: user_id: db id of user; title_id: db id of title; flag: indicate add or remove
    return: result info
    """

    try:
        role = Role.objects.get(id=role_id)
        user = User.objects.get(id=user_id)
        if flag:
            user.userinfo.role = role
            user.userinfo.save()
        else:
            user.userinfo.role = None
            user.userinfo.save()
        return "ok"
    except Exception, e:
        print e
        return "fail"


@dajaxice_register
def addOrRemoveAuth(request, perm_id, role_id, add):
    """
    JunHU
    edited:David
    summary: ajax function to add or remove connection between one auth and one title
    params: auth_id: db id of auth; title_id: db id of title; flag: indicate add or remove
    return: result info
    """
    try:
        perm = Permission.objects.get(id=perm_id)
        role = Role.objects.get(id=role_id)
        print perm, role, add
        if add:
            role.permissions.add(perm)
        else:
            role.permissions.remove(perm)
        return "ok"
    except Exception, e:
        print e
        return "fail"


@dajaxice_register
def getAuthList(request):
    """
    David
    """
    perms = GlobalPermission.objects.all()
    for perm in perms:
        perm.cate, perm.name = perm.name.split('|')
    context = {
        'perms': perms,
    }
    html = render_to_string("management/widgets/auth_table.html", context)
    return html


@dajaxice_register
def createOrDeleteAuth(request, codename=None, name=None, app_label=None, create=None):
    """
    TODO:
        Permission create or delete.
        return a signal to notify the result.
        refresh the page with ajax when it's succeed.
    ex.
    gp, created = GlobalPermission.objects.get_or_create(codename='xxx', name=u'xxx',app_label='xxx')
    gp.save()

    codename: view_storage
        用于permission_required装饰器
    name: 库存|访问库存页面
        要求严格按照格式输入，用于页面显示
    app_label: storage
        用于permission分类，值使用select标签从users.Group实例的cate域获取
    """
    pass
