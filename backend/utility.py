# coding: UTF-8
import os
import uuid

from settings import STATIC_URL, MEDIA_URL
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from const import PAGE_ELEMENTS

from backend.logging import logger, loginfo
def search_tuple(src, target):
    """
    search value in tuple
    """
    if src is None:
        return None

    for item in src:
        if item[0] == target:
            return item[1]

    return None


def convert2media_url(raw_url):
    """
    convert filefield's default url-string to media url
    example:
    convert:http://127.0.0.1:8000/media/tmp/process_file/2013/04/01/bike.jpg
    to:/static/tmp/process_file/2013....
    """
    return raw_url
    #return STATIC_URL + raw_url[raw_url.find(MEDIA_URL)+len(MEDIA_URL):]


def getContext(contentList, page=1, name="context", add_index = 1, page_elems=PAGE_ELEMENTS):
     """
     分页：
     contenList:分页内容,集合类型
     page:页码
     name:根据name获得对应的上下文名，分别为:
         #{name}_page:Page对象,默认"context_page"
         #{name}_list:第page页元素集合,默认"context_list"
     """
     paginator = Paginator(contentList, page_elems)
     try:
         _page = paginator.page(page)
     except PageNotAnInteger:
         # If page is not an integer, deliver first page.
         _page = paginator.page(1)
     except EmptyPage:
         # If page is out of range (e.g. 9999), deliver last page of results.
         _page = paginator.page(paginator.num_pages)
     page = _page.number

     single_page = (paginator.num_pages == 1)
    
     index_list = [page + x for x in xrange(-2, 3) if 1 <= page + x <= paginator.num_pages]
         # return the nearest 5 page's index number
     contain_begin = (1 in index_list)
     contain_end = (paginator.num_pages in index_list)
     _list = list(_page.object_list)
     if add_index:
         for _index in xrange(len(_list)):
             _list[_index].list_index = _index + 1 # .__dict__.update(dict)

     return {'%s_page' % name: _page,
             '%s_list' % name: _list,
             '%s_index_list'  % name: index_list,
             '%s_contain_end' % name: contain_end,
             '%s_contain_begin' % name: contain_begin,
             'single_page': single_page,
             }

def uchwidth(uch):
    """
    JunHU
    summary: calculate the display width of unicode character
    """
    if (uch >= u"\u0041" and uch <= u"\u005a") or (uch >= u"\u0061" and uch <= u"\u007a"):
        return 1
    if (uch >= u"\u0030" and uch <= u"\u0039"):
        return 1
    return 2

def rowContentGenerator(content, ROW_LEN):
    """
    JunHU
    summary: the generator to split the unicode string with constant width
    """
    row_content = u""
    row_width = 0
    if not content:
        return
    for uch in content:
        row_content += uch
        row_width += uchwidth(uch)
        if row_width == ROW_LEN or row_width == ROW_LEN - 1:
            yield row_content
            row_content = u""
            row_width = 0
    if row_content:
        yield row_content

def transferCardProcessPaginator(process_list, page, ROW_LEN = 84):
    """
    JunHU
    summary: the paginator for transfer card process list
    params: page: the page in request; ROW_LEN: the width in split row
    return: the list of RowItem 
    """
    class RowItem(object):
        def __init__(self, index = None, name = None, row_content = None):
            self.index = index
            self.name = name
            self.row_content = row_content
    
    ret_list = []
    for process in process_list:
        first_row = True
        start = 0
        for row in rowContentGenerator(process.detail, ROW_LEN):
            if first_row:
                ret_list.append(RowItem(process.index, process.name, row))
                first_row = False
            else:
                ret_list.append(RowItem(None, None, row))
            start += ROW_LEN
    total_page = 1 if len(ret_list) <= 8 else 2 + (len(ret_list) - 8 - 1) / 15
    if page > total_page:
        page = total_page

    if page == 1:
        ret_list = ret_list[0 : 8]
        while len(ret_list) < 8:
            ret_list.append(RowItem())

        return total_page, ret_list
    else:
        start_row = 8 + (page - 2) * 15
        ret_list = ret_list[start_row : start_row + 15]
        while len(ret_list) < 15:
            ret_list.append(RowItem())

        return total_page, ret_list

def make_uuid():
    """
    make uuid
    """
    return str(uuid.uuid4())



