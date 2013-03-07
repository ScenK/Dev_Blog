#!/usr/local/bin/python
#coding=utf-8

import tornado.web
from base import BaseHandler
import datetime
from Model.accounts import Account
from Model.categories import Category
from Model.tags import Tag
from lib.email_util import send_error_email
from operator import itemgetter

# Tag List_page
class TagListHandler(BaseHandler):
    def get(self, name):
        try:
            categories = Category.get()
            detail = Tag.find_by_name(name)
        except Exception as e:
            self.send_error(404)
            send_error_email('Tag List Error', str(e))

        L = detail['diaries']
        sorted_diaries = sorted(L, key=itemgetter('did'), reverse=True)
        if detail is not None:
            profile = Account.get()
            self.render('Tag/list.html', detail=detail, categories=categories, profile=profile, sorted_diaries=sorted_diaries)
        else:
            self.send_error(404)
