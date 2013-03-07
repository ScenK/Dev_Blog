#!/usr/local/bin/python
#coding=utf-8

import tornado.web
from base import BaseHandler
import datetime
from Model.accounts import Account
from Model.categories import Category
from Model.tags import Tag
from Model.calculates import Calculate
from lib.email_util import send_error_email
from operator import itemgetter

class SearchHandler(BaseHandler):
    def post(self, *args):
        try:
            keywords = self.get_argument('keywords')
        except:
            keywords = None

        if keywords is not None:
            Calculate.search_add_keyword(keywords)
            try:
                categories = Category.get()
                cate_result = Category.find_by_name(keywords)
                tag_result = Tag.find_by_name(keywords)
            except Exception as e:
                self.send_error(404)
                send_error_email('Search Error', str(e))

            try:
                C = cate_result['diaries']
            except:
                C = []

            try:
                T = tag_result['diaries']
            except:
                T = []

            real_result = list(C+T)

            """
                To combine tag_result and category_result
                first make an empty list to save filtered_result
                and to make faster, make another empty list to save diary_id to ensure not append repeat diary
            """

            filtered_result = []
            cache_did = []

            for i in real_result:
                if cache_did == []:
                    cache_did.append(i['did'])
                    filtered_result.append(i)
                else:
                    if i['did'] not in cache_did:
                        cache_did.append(i['did'])
                        filtered_result.append(i)

            profile = Account.get()

            if filtered_result != []:
                self.render('Search/result.html', detail=filtered_result, categories=categories, profile=profile)
            else:
                filtered_result = None
                self.render('Search/result.html', detail=filtered_result, categories=categories, profile=profile)
        else:
            self.redirect('/')
