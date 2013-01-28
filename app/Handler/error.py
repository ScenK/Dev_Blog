#!/usr/local/bin/python
#coding=utf-8

import tornado.web
from base import BaseHandler

class ErrorHandler(BaseHandler):
    def get(self):
        return self.send_error(404)

