#!/usr/local/bin/python
#coding=utf-8

import json
import tornado.web
from douban_client import DoubanClient
from Model.accounts import Account
from Model.diaries import Diary
from Model.categories import Category
from base import BaseHandler

class HomeHandler(BaseHandler):
    def get(self, *args):

        try:
            profile = Account.get()
            categories = Category.get()
        except Exception as e:
            print str(e)

        if profile is None:
            self.redirect('/admin')
            return

        try:
            diaries = Diary.get()
            amount = diaries.count()
        except Exception as e:
            print str(e)
            return

        number = diaries.count(with_limit_and_skip=True)

        if number == 5:
            next_page = True
        elif number < 1:
            self.send_error(404)
            return 
        else:
            next_page = False

        self.render('index.html', profile=profile, diaries=diaries, next_page=next_page, categories=categories)
