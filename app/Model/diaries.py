#!/usr/local/bin/python
#coding=utf-8

from Config.config import config as conf 
import datetime
import json
from bson import BSON
from bson import json_util
from lib.kid import Kid
import PyRSS2Gen
import markdown
from categories import Category
from tags import Tag

db = conf.site_config()['db']
conf = conf.site_config()

class Diary(object):
    def __init__(self):
        pass

    @staticmethod
    def get():
        return db.diaries.find(limit=5).sort('publish_time', -1)

    @staticmethod
    def get_detail(_id):
        return db.diaries.find_one({'_id': int(_id)})

    @staticmethod
    def del_diary(_id):
        db.diaries.remove({'_id': int(_id)})
        Category.del_diary(_id)
        return

    @staticmethod
    def update(_id, title, content, c_name, c_id, tags):
        summary = content[0:80] + '...'
        html = markdown.markdown(content)
        diary = {
                "title": title,
                "content": content,
                "category": c_name,
                "category_id": int(c_id),
                "tags": tags,
                "summary": markdown.markdown(summary),
                "html": html,
                "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

        publish_time = Diary.get_detail(_id).get('publish_time') 
        last_cid = Diary.get_detail(_id).get('category_id') 
        last_tags = Diary.get_detail(_id).get('tags') 

        db.diaries.update({'_id': int(_id)}, {'$set': diary})

        #Save for category
        Category.update_diary(c_id, _id, title, publish_time, last_cid)

        if last_tags is not None:
            # delete it from old tags
            Tag.del_diary(_id)
        
        if tags is not None:
            diary = Diary.get_detail(_id)
            # save tags
            for tag in tags:
                Tag.add(tag, diary)
        return 

    #Design For Link Douban Diary 
    @staticmethod
    def get_by_id(id):
        exist = db.diaries.find_one({'id': id})
        if exist is None:
            return None
        else:
            return 'exist'

    @staticmethod
    def load_more(offset):
        more = db.diaries.find(limit=3).skip(offset).sort('publish_time', -1)
        collection = []
        for i in more:
            collection.append(json.dumps(i, sort_keys=True, indent=4, 
                              default=json_util.default))
        return collection

    @staticmethod
    def add(title, content, c_name, c_id, tags):
        summary = content[0:80] + '...'
        html = markdown.markdown(content)

        diary = {
                "_id": Kid.kid(),
                "title": title,
                "category": c_name,
                "category_id": int(c_id),
                "tags": tags,
                "content": content,
                "html": html,
                "summary": markdown.markdown(summary),
                "publish_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        db.diaries.save(diary)

        # save category
        Category.update_diary(c_id, diary.get('_id'), title, diary.get('publish_time'))

        if tags is not None:
            # save tags
            for tag in tags:
                Tag.add(tag, diary)
        return 

    @staticmethod
    def set_date(_id, time):
        diaries = db.diaries

        diary = {"publish_time": time}

        db.diaries.update({'_id': int(_id)}, {'$set': diary})
        return 

    @staticmethod
    def output_rss():
        articles = db.diaries.find(limit=12).sort('publish_time', -1)
        items = []
        for article in articles:
            content = ''
            if article.get('html') is not None:
                content = article.get('html')
            else:
                content = article.get('content')

            url = conf['url'] + '/diary/detail/' + str(article.get('_id'))
            items.append(PyRSS2Gen.RSSItem(
                title = article.get('title'),
                link = url,
                description = content,
                guid = PyRSS2Gen.Guid(url),
                pubDate = article.get('publish_time'),
            ))
        rss = PyRSS2Gen.RSS2(
            title = conf['title'],
            link = conf['url'],
            description = conf['description'],
            lastBuildDate = datetime.datetime.now(),
            items = items
        ).to_xml('utf-8')
        return rss

    @staticmethod
    def get_diary_count():
        return db.diaries.count() 

    @staticmethod
    def get_last_diary():
        return db.diaries.find(limit=1).sort('publish_time', -1) 

    @staticmethod
    def get_first_diary():
        return db.diaries.find(limit=1).sort('publish_time', 1) 

    @staticmethod
    def get_diary_list(page):
        return db.diaries.find(limit=5).skip((int(page)-1)*5).sort('publish_time', -1)
