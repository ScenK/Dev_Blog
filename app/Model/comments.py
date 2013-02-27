#!/usr/local/bin/python
#coding=utf-8

import datetime
from diaries import Diary
from lib.kid import Kid
from Config.config import config as conf 

db = conf.site_config()['db']

class Comment(object):
    def __init__(self):
        pass

    @staticmethod
    def save(did, user, email, content):
    
        diary_detail = Diary.get_detail(did)

        # init comments_count in single-diary
        comments_count = diary_detail.get('comments_count')
        if comments_count is None:
            comments_count = 0

        comment = {
                "_id": Kid.kid(), 
                "did": int(did),
                "user": user,
                "email": email,
                "content": content,
                "publish_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

        db.diaries.update({'_id': int(did)}, {'$inc': {'comments_count': 1}, 
                                         '$push': {'comment': comment}})

        # Save in Comments Collection for Admin 
        diary_title = diary_detail.get('title')
        comment['diary_title'] = diary_title
        db.comments.save(comment)
        return

    @staticmethod
    def get(offset):
        return db.comments.find(limit=15).skip((int(offset)-1)*15).sort('publish_time', -1)

    @staticmethod
    def del_comment(did, _id):
        db.comments.remove({'_id': int(_id)})

        # Change in Frontend Interface
        db.diaries.update({'_id': int(did)}, {'$pull': {'comment': {'_id': int(_id)}} 
                                            ,'$inc': {'comments_count': -1}})
        return

    @staticmethod
    def reply(did, cid, content):

        comment = {
                "_id": Kid.kid(), 
                "did": int(did),
                "parent_id": int(cid),
                "user": "博主回复",
                "content": content,
                "publish_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

        db.diaries.update({'_id': int(did)}, {'$inc': {'comments_count': 1}, 
                                         '$push': {'comment': comment}})

        # Save in Comments Collection for Admin 
        diary_detail = Diary.get_detail(did)
        diary_title = diary_detail.get('title')
        comment['diary_title'] = diary_title
        db.comments.save(comment)
        return

    @staticmethod
    def get_comment_count():
        return db.comments.count() 
