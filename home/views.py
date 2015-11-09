# coding: UTF-8
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators import csrf

from backend.utility import getContext

from news.models import *
from const import *

def index_context(request):
	news_company_news = News.objects.filter(news_category__category = NEWS_CATEGORY_COMPANYNEWS).order_by('-news_date')
	news_import_info = News.objects.filter(news_category__category = NEWS_CATEGORY_IMPORTINFO).order_by('-news_date')
	homepage_docs = DocumentFile.objects.filter(news__isnull = False).order_by('-news__news_date')
	context = getContext(news_company_news, 1, "news_company_news")
	context.update(getContext(news_import_info, 1 , "news_import_info"))
	context.update(getContext(homepage_docs, 1, "homepage_docs"))
	return context

def homepageViews(request):
	# news_company_news = News.objects.filter(news_category__category = NEWS_CATEGORY_COMPANYNEWS).order_by('-news_date')
	# news_import_info = News.objects.filter(news_category__category = NEWS_CATEGORY_IMPORTINFO).order_by('-news_date')
	# homepage_docs = DocumentFile.objects.filter(news__isnull = False).order_by('-news__news_date')
	context = {}

	context.update(index_context(request))
    
	news_cate = {}
	news_cate["news_category_companynews"] = NEWS_CATEGORY_COMPANYNEWS
	news_cate["news_category_importinfo"] = NEWS_CATEGORY_IMPORTINFO
	news_cate["news_category_document"] = NEWS_CATEGORY_DOCUMENTS
	# context = {
 #    			"news_company_news_list" : news_company_news,
 #    			"news_import_info_list" : news_import_info,
 #    			"homepage_docs_list" : homepage_docs
 #    		}
	context.update(news_cate)
	return render(request,"home/homepage.html",context)
