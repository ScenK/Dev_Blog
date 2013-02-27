#!/usr/local/bin/python
#coding=utf-8

import datetime
from diaries import Diary
from lib.kid import Kid
from Config.config import config as conf 

db = conf.site_config()['db']

class Tag(object):
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
                "did": did,
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
