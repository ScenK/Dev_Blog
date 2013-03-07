#!/usr/local/bin/python
#coding=utf-8

import datetime
from lib.kid import Kid
from Config.config import config as conf

db = conf.site_config()['db']

class Calculate(object):
    def __init__(self):
        pass

    @staticmethod
    def search_add_keyword(name):
        if Calculate.search_find_by_keyword(name) is None:
            keyword = {
                       "_id": Kid.kid(),
                       "name": name,
                       "count": 1,
                       "publish_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                      }
            return db.cal_search_words.save(keyword)
        else:
            return db.cal_search_words.update({'name': name}, {'$inc': {'count': 1}})

    @staticmethod
    def search_find_by_keyword(name):
        return db.cal_search_words.find_one({'name': name})
