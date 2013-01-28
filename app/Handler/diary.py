#!/usr/local/bin/python
#coding=utf-8

import tornado.web
from Model.accounts import Account
from Model.diaries import Diary
from Model.comments import Comment
from base import BaseHandler
import json
from lib.email_util import send_error_email

# Diarydetail Page
class DiaryDetailHandler(BaseHandler):
    def get(self, _id):
        try:
            detail = Diary.get_detail(_id)
        except Exception as e:
            self.send_error(404)
            send_error_email('Diary Detail Error', str(e))

        if detail is not None:
            profile = Account.get()
            try:
               guest_name = self.get_secure_cookie('guest_name')
               guest_email = self.get_secure_cookie('guest_email')
            except:
               guest_name = None
               guest_email = None

            self.render('Diary/detail.html', detail=detail, profile=profile, guest_name=guest_name, guest_email=guest_email)
        else:
            self.send_error(404)



class DiaryListHandler(BaseHandler):
    def get(self, page):

        try:
            profile = Account.get()
            diaries = Diary.get_diary_list(page)
        except Exception as e:
            self.send_error(404)
            send_error_email('Diary List Error', str(e))

        number = diaries.count(with_limit_and_skip=True)

        if number == 15:
            next_page = True
        elif number < 1:
            self.send_error(404)
            return 
        else:
            next_page = False

        self.render('Diary/list.html', diaries=diaries, profile=profile, page=page, next_page=next_page)

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
