#!/usr/local/bin/python
#coding=utf-8

import json
import tornado.web
from douban_client import DoubanClient
from Model.accounts import Account
from Model.diaries import Diary
from base import BaseHandler

class HomeHandler(BaseHandler):
    def get(self, *args):

        try:
            profile = Account.get()
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

        if amount >= 5:
            amount = 5

        self.render('index.html', profile=profile, diaries=diaries, amount=amount)
