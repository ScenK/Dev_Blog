#!/usr/local/bin/python
#coding=utf-8

import tornado.web
from Model.accounts import Account
from Model.diaries import Diary
from Model.comments import Comment
from base import BaseHandler
import json

# Diarydetail Page
class DiaryDetailHandler(BaseHandler):
    def get(self, _id):
        try:
            detail = Diary.get_detail(_id)
            profile = Account.get()
        except Exception as e:
            print str(e)

        try:
            guest_name = self.get_secure_cookie('guest_name')
            guest_email = self.get_secure_cookie('guest_email')
        except:
            guest_name = None
            guest_email = None

        self.render('Diary/detail.html', detail=detail, profile=profile, guest_name=guest_name, guest_email=guest_email)


class DiaryListHandler(BaseHandler):
    def get(self, page):

        try:
            profile = Account.get()
            diaries = Diary.get_diary_list(page)
            number = Diary.get_diary_count()
        except Exception as e:
            print str(e)

        if number % 15 == 0:
            limit = number / 15
        else:
            limit = number / 15 + 1

        self.render('Diary/list.html', diaries=diaries, profile=profile, page=page, limit=limit)

# AJAX Diary Load_action
class DiaryLoadHandler(BaseHandler):
    def get(self, *args):
        
        offset = int(self.get_argument('offset'))

        try:
          more = Diary.load_more(offset)
        except Exception as e:
            print str(e)

        self.write(json.dumps(more)) 

# RSS 
class DiaryRssHandler(BaseHandler):
    def get(self):
        try:
            rss = Diary.output_rss()
        except Exception as e:
            print str(e)

        self.render('rss.html', rss=rss)
