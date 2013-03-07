#!/usr/local/bin/python
#coding=utf-8

import datetime
from lib.kid import Kid
from Config.config import config as conf 

db = conf.site_config()['db']

class Tag(object):
    def __init__(self):
        pass

    @staticmethod
    def get():
      return db.tags.find()

    @staticmethod
    def find_by_name(name):
        return db.tags.find_one({'name': name})

    @staticmethod
    def add(tag, diary):

        exist_tag = Tag.find_by_name(tag)

        """ first determine whether there is an exist tag
            if there is, update from old tag then add diary in it,
            else, create a new tag
        """

        if exist_tag is None:
            new_tag = {
                       "_id": Kid.kid(),
                       "name": tag,
                       "diaries_num": 0,
                       "publish_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                      }

            db.tags.save(new_tag)
            tid = new_tag.get('_id')
        else:
            tid = exist_tag.get('_id')

        Tag.add_diary(tid, diary.get('_id'), diary.get('title'), diary.get('publish_time'))
        return

    @staticmethod
    def add_diary(_id, did, title, dtime):

        diary = {
                "_id": Kid.kid(),
                "did": int(did),
                "title": title,
                "publish_time": dtime
              }

        return db.tags.update({'_id': int(_id)}, {'$inc': {'diaries_num': 1}, '$push': {'diaries': diary}})

    @staticmethod
    def find_by_id(_id):
        return db.tags.find_one({'_id': int(_id)})

    @staticmethod
    def del_diary(did):
        return db.tags.update({'diaries.did': int(did)}, {'$inc': {'diaries_num': -1}, '$pull': {'diaries': {'did': int(did)}}})
