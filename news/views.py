# Create your views here.
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse, Http404
import json
from django.db import transaction
import os
from backend.utility import getContext

from news.models import *
from const import *

def get_news(news_id = None):
	if news_id:
		try:
			news_content = News.objects.get(id = news_id)
		except:
			raise Http404
	return news_content

def get_docs(news_id):
	docs = DocumentFile.objects.filter(news__id = news_id)
	return docs

def read_news(request, news_id):
	# print news_id
	news = get_news(news_id)
	news_cate = news.news_category
	news_docs = get_docs(news_id)
	context = {
		'news' : news,
		'news_cate' : news_cate,
		'news_docs' : news_docs
	}
	return render(request, 'home/news-content.html', context)

def list_news_by_cate(request, news_cate):
	try:
		if news_cate == NEWS_CATEGORY_DOCUMENTS:
			news_list = DocumentFile.objects.filter(news__isnull = False).order_by('-news__news_date')
			html = 'home/docs-list.html'
		else:
			news_list = News.objects.filter(news_category__category = news_cate).order_by('-news_date')
			html = 'home/news-list-by-cate.html'
	except:
		raise Http404
	news_page = request.GET.get('news_page')
	context = getContext(news_list, news_page, 'news')
	# context = {
	# 	'news_list' : news_list,
	# 	'news_cate' : news_cate
	# }
	context["news_cate"] = news_cate
	return render(request, html, context)

BUF_SIZE = 262144
def download_news_doc(request, docs_id):
    news_doc_name = DocumentFile.objects.get(id = docs_id).news_document.path
    # print news_doc_name
    # print os.path.basename(news_doc_name)
    def readFile(fn, buf_size = BUF_SIZE):
    	f = open(fn, "rb")
    	while True:
    		_c = f.read(buf_size)
    		if _c:
    			yield _c
    		else:
    			break
    	f.close()
    # response = HttpResponse(readFile(news_doc_name), content_type = 'application/vnd.ms-excel')
    response = HttpResponse(readFile(news_doc_name), mimetype = 'application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(news_doc_name).encode("UTF-8")
    return response
