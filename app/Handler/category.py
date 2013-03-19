#!/usr/local/bin/python
#coding=utf-8

import tornado.web
from base import BaseHandler
import datetime
from Model.categories import Category
from Model.accounts import Account
from lib.email_util import send_error_email
from operator import itemgetter

# Category List_page
class CategoryListHandler(BaseHandler):
    def get(self, _id):
        try:
            categories = Category.get()
            detail = Category.find_by_id(_id)
        except Exception as e:
            self.send_error(404)
            send_error_email('Category List Error', str(e))

        L = detail['diaries']
        sorted_diaries = sorted(L, key=itemgetter('did'), reverse=True) 

        number = len(sorted_diaries)

        if number == 15:
            next_page = True
        elif number < 1:
            self.send_error(404)
            return 
        else:
            next_page = False

        if detail is not None:
            profile = Account.get()
            self.render('Category/list.html', detail=detail, categories=categories, profile=profile, sorted_diaries=sorted_diaries, next_page=next_page, cid=_id)
        else:
            self.send_error(404)

# Category List Paging
class CategoryPagingHandler(BaseHandler):
    def get(self, cid, page):
        try:
            categories = Category.get()
            detail = Category.find_by_id(cid, page)
        except Exception as e:
            self.send_error(404)
            send_error_email('Category List Error', str(e))

        L = detail['diaries']
        sorted_diaries = sorted(L, key=itemgetter('did'), reverse=True) 

        number = len(sorted_diaries)

        if number == 15:
            next_page = True
        elif number < 1:
            self.send_error(404)
            return 
        else:
            next_page = False

        if detail is not None:
            profile = Account.get()
            self.render('Category/list.html', detail=detail, categories=categories, profile=profile, sorted_diaries=sorted_diaries, page=page, next_page=next_page, cid=cid)
        else:
            self.send_error(404)
