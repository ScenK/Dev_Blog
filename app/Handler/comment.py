#!/usr/local/bin/python
#coding=utf-8

import tornado.web
from base import BaseHandler
from Model.comments import Comment
from lib.email_util import send_mail, generateHtml
import datetime
from Config.config import config as conf

conf = conf.site_config()

# Diary add_comment
class CommentAddHandler(BaseHandler):
    def post(self, *args):
        try:
            did = self.get_argument('did')
            user = self.get_argument('username')
            email = self.get_argument('email')
            comment = self.get_argument('comment')
        except Exception as e:
            print str(e)

        Comment.save(did, user, email, comment)
        self.set_secure_cookie("guest_name", user)
        self.set_secure_cookie("guest_email", email)

        try:
            send_mail(conf['email'], conf['title']+'收到了新的评论, 请查收', comment, did, user)
            self.write('success')
        except Exception as e:
            print str(e)

# Comments_action
class CommentDelHandler(BaseHandler):
    def post(self, *args):

        did = self.get_argument('did')
        _id = self.get_argument('cid')

        try:
            Comment.del_comment(did, _id)
        except Exception as e:
            print str(e)

# Comments_reply_action
class CommentReplyHandler(BaseHandler):
    def post(self, *args):

        did = self.get_argument('did')
        cid = self.get_argument('cid')
        receiver = self.get_argument('email')
        title = self.get_argument('title')
        content = self.get_argument('content')
        user = self.get_argument('user')

        try:
            Comment.reply(did, cid, content)
        except Exception as e:
            print str(e)

        try:
            send_mail(receiver, u'您评论的文章《'+title+u'》收到了来自博主的回复, 请查收', content, did, user)
            self.write('success')
        except Exception as e:
            print str(e)

