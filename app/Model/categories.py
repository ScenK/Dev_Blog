#!/usr/local/bin/python
#coding=utf-8

import datetime
from lib.kid import Kid
from Config.config import config as conf 

db = conf.site_config()['db']

class Category(object):
    def __init__(self):
        pass

    @staticmethod
    def get():
      return db.categories.find().sort('publish_time', -1)

    @staticmethod
    def new(cat):
      categories = db.categories

      category = {
                  "_id": Kid.kid(),
                  "name": cat,
                  "diaries_num": 0,
                  "publish_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

      categories.save(category)
      return category.get('_id')

    @staticmethod
    def find_by_name(name):
        return db.categories.find_one({'name': name})

    @staticmethod
    def update_diary(_id, did, title, dtime, last_id=None):

        """ first determine whether there is an exist diary
            if there is, delete it from old category then create it in new category,
            else, create it
        """
        
        if last_id is not None:
            Category.del_diary(did)

        diary = {
                "_id": Kid.kid(),
                "did": int(did),
                "title": title,
                "publish_time": dtime
              }

        db.categories.update({'_id': int(_id)}, {'$inc': {'diaries_num': 1}, '$push': {'diaries': diary}})
        return

    @staticmethod
    def find_by_id(_id, page=1):
        return db.categories.find_one({'_id': int(_id)}, {'diaries': {'$slice': [-15+int(page)*15, 15]}})

    @staticmethod
    def find_all_by_id(_id):
        return db.categories.find_one({'_id': int(_id)})

    @staticmethod
    def del_diary(did):
        return db.categories.update({'diaries.did': int(did)}, {'$inc': {'diaries_num': -1}, '$pull': {'diaries': {'did': int(did)}}})

    @staticmethod
    def del_category(_id):
       
        """ del category make all diaries return into category=>undefined
            and del this category
        """
        diaries = Category.find_all_by_id(_id).get('diaries')
        """ try to move diaries into categpry=>undefined
            if categpry=>undefined is not exist, create it first
            else move into immediately
        """
        if Category.find_by_name('未分类'):
            new_c_id = Category.find_by_name('未分类').get('_id')
        else:
            new_c_id = Category.new('未分类')

        for i in diaries:
            did = i.get('did')
            title = i.get('title')
            dtime = i.get('publish_time')
            Category.update_diary(new_c_id, did, title, dtime)
                
        db.categories.remove({'_id': int(_id)})

