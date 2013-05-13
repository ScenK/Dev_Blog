#!/usr/local/bin/python
#coding=utf-8

import datetime
from lib.kid import Kid
from Config.config import config as conf
import markdown

db = conf.site_config()['db']

class Page(object):
    def __init__(self):
        pass

    @staticmethod
    def get():
        return db.pages.find()

    @staticmethod
    def find_by_property(property):
        return db.pages.find_one({'property': property})

    @staticmethod
    def find_by_id(_id):
        return db.pages.find_one({'_id': int(_id)})

    @staticmethod
    def del_page(_id):
        return db.pages.remove({'_id': int(_id)})

    @staticmethod
    def new(title, content, property):
        html = markdown.markdown(content)

        detail = {
                "_id": Kid.kid(),
                "title": title,
                "property": property,
                "content": content,
                "html": html,
                "publish_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

        db.pages.save(detail)
        return

    @staticmethod
    def update(_id, title, content, property):
        html = markdown.markdown(content)

        detail = {
                "title": title,
                "property": property,
                "content": content,
                "html": html,
                "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

        db.pages.update({'_id': int(_id)}, {'$set': detail})
        return
