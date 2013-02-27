#!/usr/local/bin/python
#coding=utf-8

import json
import tornado.web
from base import BaseHandler
from Model.accounts import Account
from Model.gallaries import Gallary
from lib.email_util import send_error_email
import json

class GallaryHandler(BaseHandler):
    def get(self, *args):
        try:
            albums = Gallary.get_all()
            profile = Account.get()
        except Exception as e:
            self.send_error(404)
            send_error_email('Gallary get Error', str(e))

        self.render('Gallary/index.html', albums=albums, profile=profile)
