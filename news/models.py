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
	message = models.ForeignKey(Message, blank = True, null = True, verbose_name = "消息")

	def __unicode__(self):
		return news_document.filename

	class Meta:
		verbose_name = "文件"
		verbose_name_plural = u"文件"

class Message(models.Model):
	title = models.CharField(max_length = 100, verbose_name = "标题")
	content = models.TextField( verbose_name = "内容")
	writer = modeks.foreignKey(User, "发信人")
	time = models.DateTimeField(verbose_name = "时间")
	
	class Meta:
		verbose_name = u"消息"
		verbose_name_plural = u"消息"
	def __unicode__(self):
		return self.title

class  MessageBox(models.Model):
	user = models.OneToOneField(User, verbose_name = "用户")
	message = models.ForeignKey(Message, verbose_name = "消息")
	read = models.BooleanField(verbose_name = "是否阅读")

	class Meta:
		verbose_name = u"信箱"
		verbose_name_plural = u"信箱"
	def __unicode__(self):
		return self.user

