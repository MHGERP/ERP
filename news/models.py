# coding: UTF-8
from django.db import models
import datetime, os
from settings import NEWS_DOCUMENTS_PATH

from news import NEW_CATEGORY_CHOICES, NEWS_CATEGORY_COMPANYNEWS

# Create your models here.

class NewsCategory(models.Model):
    category = models.CharField(blank=False, null=False,unique=True,max_length=20,
                                choices = NEW_CATEGORY_CHOICES, \
                                default = NEWS_CATEGORY_COMPANYNEWS ,
                                verbose_name = u"新闻类型")

    class Meta:
    	verbose_name = "新闻类型"
    	verbose_name_plural = "新闻类型"

    def __unicode__(self):
    	return self.get_category_display()


class News(models.Model):
	news_title = models.CharField(verbose_name = u"标题", blank=True, max_length=200)
	news_content = models.TextField(verbose_name = u"新闻内容", blank=True)
	news_date = models.DateField(verbose_name = u"发表时间", default=datetime.datetime.today, blank=True)
	news_category = models.ForeignKey(NewsCategory, verbose_name = u"新闻类型", blank=True, null=True)

	def __unicode__(self):
		return self.news_title

	class Meta:
	    verbose_name = "新闻"
	    verbose_name_plural = "新闻"

class DocumentFile(models.Model):
	news_document = models.FileField(upload_to=NEWS_DOCUMENTS_PATH, null = False, blank = False)
	news = models.ForeignKey(News, verbose_name = u"", blank = True, null = True)

	def __unicode__(self):
		return news_document.filename

	class Meta:
		verbose_name = "文件"
		verbose_name_plural = u"文件"
