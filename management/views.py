# coding: UTF-8
from django.shortcuts import render
from const.forms import InventoryTypeForm
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
import json
from django.db import transaction

from news.forms import NewsForm, MessageForm
from news.models import News, DocumentFile, NewsCategory

from forms import GroupForm
from users.models import Title

def userManagementViews(request):
    """
    JunHU
    """
    form = GroupForm()
    context = {
            "form": form,
    }
    return render(request, "management/user_management.html", context)

def groupManagementViews(request):
    """
    JunHU
    """
    context = {}
    return render(request, "management/group_management.html", context)

def titleManagementViews(request):
    """
    JunHU
    """
    form = GroupForm()
    context = {
            "form": form,
        }
    return render(request, "management/title_management.html", context)

def messageManagementViews(request):
    """
    JunHU
    """
    messageform = MessageForm()
    context = {
        "messageform": messageform
    }
    return render(request, "management/message_management.html", context)

def authorityManagementViews(request):
    """
    JunHU
    """
    title_id = request.GET.get("title_id")
    title = Title.objects.get(id = title_id)
    context = {
            "title": title,
        }
    return render(request, "management/authority_management.html", context)


def newsReleaseViews(request):
    """
    mxl
    """
    if request.method == 'POST':
        files = request.FILES.getlist("news_document")
        newsform = NewsForm(request.POST)
        if newsform.is_valid():
            new_news = News(news_title = newsform.cleaned_data["news_title"],
                             news_content = newsform.cleaned_data["news_content"],
                             news_date = newsform.cleaned_data["news_date"],
                             news_category = NewsCategory.objects.get(id = newsform.cleaned_data["news_category"])
                            )
            new_news.save()
        if files:
            for f in files:
                doc = DocumentFile(news_document = f,
                                    news = new_news)
                doc.save()
        return redirect(request,"news/newslist/%s" % new_news.id)
    else:
        newsform = NewsForm()
        context = {
            'newsform' : newsform
        }
        return render(request, "management/news_release.html", context)
