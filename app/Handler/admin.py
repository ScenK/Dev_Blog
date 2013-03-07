#!/usr/local/bin/python
#coding=utf-8

import tornado.web
from base import BaseHandler
from weibo import APIClient
from Model.admins import Admin
from Model.diaries import Diary
from Model.comments import Comment
from Model.gallaries import Gallary
from Model.categories import Category
from Model.tags import Tag
import json

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
        except Exception as e:
            print str(e)

        number = diaries.count(with_limit_and_skip=True)
        if number == 5:
            next_page = True
        elif number < 1:
            self.send_error(404)
            return 
        else:
            next_page = False

        self.render('Admin/Diary/list.html', diaries=diaries, page=page, next_page=next_page)

# Categorys_page 
class AdminCategoryHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        try:
            categories = Category.get()
        except Exception as e:
            print str(e)

        self.render('Admin/Category/index.html', categories=categories)

# Comments_page 
class AdminCommentHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page):
        
        try:
            comments = Comment.get(page)
        except Exception as e:
            print str(e)

        number = comments.count(with_limit_and_skip=True)
        if number == 15:
            next_page = True
        elif number < 1:
            self.send_error(404)
            return 
        else:
            next_page = False

        self.render('Admin/Comment/index.html', comments=comments, page=page, next_page=next_page)

# Diary Add_action
class DiaryAddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        categories = Category.get()
        self.render('Admin/Diary/add.html', categories=categories)

    @tornado.web.authenticated
    def post(self, *args):

        try:
            title = self.get_argument('title')
            content = self.get_argument('content')
            c_name = self.get_argument('category_name')
            c_id = self.get_argument('c_id')
        except:
            self.redirect('/diary/add')

        try:
            tags = self.get_argument('tags')
        except:
            tags = None

        if tags:
            splited_tags = tags.split(',')
        else:
            splited_tags = None

        """" determin whether there is a exist undefine category
             if there is not, create it
             else use its c_id
        """
        if c_id == 'none':
            detail = Category.find_by_name(c_name)
            try:
                c_id = detail.get('_id')
            except:
                c_id = Category.new(c_name) 

        try:
            Diary.add(title, content, c_name, c_id, splited_tags)
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
            categories = Category.get()
        except:
            self.redirect('/admin')

        self.render('Admin/Diary/edit.html', detail=detail, categories=categories)

    @tornado.web.authenticated
    def post(self, *args):
        
        try:
            did = self.get_argument('did')
            title = self.get_argument('title')
            content = self.get_argument('content')
            c_name = self.get_argument('category_name')
            c_id = self.get_argument('c_id')
        except Exception as e:
            refer = self.request.headers.get('Referer')
            self.redirect(refer)
        
        try:
            tags = self.get_argument('tags')
        except:
            tags = None

        if tags:
            splited_tags = tags.split(',')
        else:
            splited_tags = None

        """" determin whether there is a exist undefine category
             if there is not, create it
             else use its c_id
        """
        if c_id == 'none':
            detail = Category.find_by_name(c_name)
            try:
                c_id = detail.get('_id')
            except:
                c_id = Category.new(c_name) 
        try:
            Diary.update(did, title, content, c_name, c_id, splited_tags)
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

# Diary add_photo_action
class DiaryAddPhotoHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args):
        data = self.request.files['userfile']
        try:
          url = Gallary.up_to_upyun('diary', data[0])
          self.write('![](%s)' % str(url))
        except Exception as e:
          print str(e)

# Gallary_page 
class AdminGallaryHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        gallaries = Gallary.get_all()
        self.render('Admin/Gallary/index.html', gallaries=gallaries)

# Gallary_add_page 
class AdminGallaryAddHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args):
        title = self.get_argument('title')
        desc = self.get_argument('desc')
        try:
            Gallary.add(title, desc)
        except Exception as e:
          print str(e)

# Gallary_detail_page 
class AdminGallaryDetailHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, _id):
        try:
            photos = Gallary.get_detail(_id)
            self.render('Admin/Gallary/detail.html', photos=photos, gid=_id)
        except Exception as e:
          print str(e)

# Gallary_add_photo_action 
class AdminGallaryAddPhotoHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args):
        files = self.request.files['qqfile']
        gid = self.get_argument('gid')
        for i in files:
            try:
              url = Gallary.up_to_upyun('gallary', i)
              if url:
                  Gallary.save_photo(gid, url, i.get('filename'))
                  self.write(json.dumps({'success': 'true'}))
              else:
                  self.write(json.dumps({'success': 'false'}))
            except Exception as e:
              print str(e)

# Category_new_action 
class AdminCategoryAddHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args):
        category = self.get_argument('category')

        try:
          cid = Category.new(category)
        except Exception as e:
          print str(e)

        if cid:
          self.write(json.dumps({'success': 'true', 'cid': cid}))
        else:
          self.write(json.dumps({'success': 'false'}))
