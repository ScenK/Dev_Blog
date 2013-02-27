#!/usr/local/bin/python
#coding=utf-8

import tornado.web
from base import BaseHandler
from Model.categories import Category

class AboutHandler(BaseHandler):
    def get(self):
        try:
            categories = Category.get()
        except Exception as e:
            print str(e)

        self.render('about.html', categories=categories)

