# coding: UTF-8
from django.db import models
import datetime, os
from settings import NEWS_DOCUMENTS_PATH

from const import NEW_CATEGORY_CHOICES, NEWS_CATEGORY_COMPANYNEWS
from django.contrib.auth.models import User

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
	    verbose_name = u"新闻"
	    verbose_name_plural = u"新闻"

class Message(models.Model):
	title = models.CharField(max_length = 100, verbose_name = u"标题")
	content = models.TextField( verbose_name = u"内容")
	writer = models.ForeignKey(User, verbose_name = u"发信人")
	time = models.DateTimeField(verbose_name = u"时间")
	
	class Meta:
		verbose_name = u"消息"
		verbose_name_plural = u"消息"
	def __unicode__(self):
		return self.title

class  MessageBox(models.Model):
	user = models.OneToOneField(User, verbose_name = u"用户")
	message = models.ForeignKey(Message, verbose_name = u"消息")
	read = models.BooleanField(verbose_name = u"是否阅读")

	class Meta:
		verbose_name = u"信箱"
		verbose_name_plural = u"信箱"
	def __unicode__(self):
		return ""

class DocumentFile(models.Model):
	news_document = models.FileField(upload_to=NEWS_DOCUMENTS_PATH, null = False, blank = False, verbose_name = u"文件")
	news = models.ForeignKey(News, blank = True, null = True, verbose_name = u"新闻")
	message = models.ForeignKey(Message, blank = True, null = True, verbose_name = u"消息")

	def document_name(self):
		return os.path.basename(self.news_document.name)

	def __unicode__(self):
		return os.path.basename(self.news_document.name)

	class Meta:
		verbose_name = "文件"
		verbose_name_plural = u"文件"


