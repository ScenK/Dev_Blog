#!/usr/local/bin/python
#coding=utf-8

import tornado.web
from base import BaseHandler
from Model.categories import Category
from Model.pages import Page

class AboutHandler(BaseHandler):
    def get(self):
        try:
            categories = Category.get()
            content = Page.find_by_property('about')
        except Exception as e:
            print str(e)

        self.render('about.html', categories=categories, content=content)

