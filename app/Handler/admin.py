#!/usr/local/bin/python
#coding=utf-8

import tornado.web
from base import BaseHandler
from weibo import APIClient
from Model.admins import Admin
from Model.diaries import Diary
from Model.comments import Comment

from douban_client import DoubanClient
from Config.config import config as conf 

conf = conf.site_config()

# Login_page
class LoginHandler(BaseHandler):
    def get(self):
        self.render('Admin/login.html')

    def post(self, *args):

        try:
            usr = self.get_argument('username')
            pas = self.get_argument('password')
        except:
            self.redirect('/login')

        try:
            rem = self.get_argument('remember')
        except:
            rem = None

        profile = Admin.find_by_username(usr)

        if profile is not None and pas == profile.get('password'):

            # Set Cookie or Session
            if rem is not None: 
                self.set_secure_cookie("user", profile.get('user'))
            else:
                self.set_secure_cookie("user", profile.get('user'), expires_days=None)

            self.redirect('/admin')
        else:
            self.redirect('/login')

# Logout
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

# Dashboard_page
class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # OAth2 for douban
        KEY = conf['douban_app_key']
        SECRET = conf['douban_app_secret']
        CALLBACK = conf['url'] + '/dback'
        SCOPE = 'douban_basic_common,community_basic_user,community_basic_note'
        client = DoubanClient(KEY, SECRET, CALLBACK, SCOPE)
        douban_login = client.authorize_url

        # OAth2 for sina_weibo
        APP_KEY =  conf['weibo_app_key']
        APP_SECRET = conf['weibo_app_secret']
        CALLBACK_URL = conf['url'] + '/wback'
        weibo_client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        weibo_login = weibo_client.get_authorize_url()

        # statistics
        diary_count = Diary.get_diary_count()
        last_diary = Diary.get_last_diary()
        first_diary = Diary.get_first_diary()
        comment_count = Comment.get_comment_count()

        usr = tornado.escape.xhtml_escape(self.current_user)  
        site_start = Admin.find_by_username(usr).get('site_start')
        self.render('Admin/dashboard.html', douban_login=douban_login,
                    diary_count=diary_count, last_diary=last_diary,
                    first_diary=first_diary, site_start=site_start,
                    comment_count=comment_count, weibo_login=weibo_login
                  )

# Diarylist_page
class AdminDiaryListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page):

        try:
            diaries = Diary.get_diary_list(page)
            number = Diary.get_diary_count()
        except Exception as e:
            print str(e)

        if number % 15 == 0:
            limit = number / 15
        else:
            limit = number / 15 + 1

        self.render('Admin/Diary/list.html', diaries=diaries, page=page, limit=limit)

# Settings_page 
class AdminSettingsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('Admin/Settings/index.html')

# Comments_page 
class AdminCommentHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page):
        
        try:
            comments = Comment.get(page)
            number = Comment.get_comment_count()
        except Exception as e:
            print str(e)

        if number % 15 == 0:
            limit = number / 15
        else:
            limit = number / 15 + 1

        self.render('Admin/Comment/index.html', comments=comments, page=page, limit=limit)

# Diary Add_action
class DiaryAddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('Admin/Diary/add.html')

    @tornado.web.authenticated
    def post(self, *args):

        try:
            title = self.get_argument('title')
            content = self.get_argument('content')
        except:
            self.redirect('/diary/add')

        try:
            Diary.add(title, content)
        except Exception as e:
            print str(e)
        
        self.redirect('/admin/all-post/1')

# Diary Del_action
class DiaryDelHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, _id):

        try:
            detail = Diary.del_diary(_id)
        except Exception as e:
            print str(e)

        self.redirect('/admin/all-post/1')

# Diary Update_action
class DiaryUpdateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, _id):

        try:
            detail = Diary.get_detail(_id)
        except:
            self.redirect('/admin')

        self.render('Admin/Diary/edit.html', detail=detail)

    @tornado.web.authenticated
    def post(self, *args):
        
        try:
            did = self.get_argument('did')
            title = self.get_argument('title')
            content = self.get_argument('content')
        except Exception as e:
            print str(e)
        
        try:
            Diary.update(did, title, content)
        except Exception as e:
            print str(e)

        self.redirect('/admin/all-post/1')

# Diary Change_publish_date_action
class DiarySetDateHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args):
        try:
            did = self.get_argument('did')
            date = self.get_argument('date')
        except Exception as e:
            print str(e)

        try:
            Diary.set_date(did, date)
            self.write('success')
        except Exception as e:
            print str(e)
