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
from lib.upyun import UpYun,md5,md5file

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
        return

    @staticmethod
    def update(_id, title, content):
        summary = content[0:80] + '...'
        html = markdown.markdown(content)
        diary = {
                "title": title,
                "content": content,
                "summary": summary,
                "html": html,
                "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        db.diaries.update({'_id': int(_id)}, {'$set': diary})
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
    def add(title, content):
        diaries = db.diaries

        summary = content[0:80] + '...'
        html = markdown.markdown(content)

        diary = {
                "_id": Kid.kid(),
                "title": title,
                "content": content,
                "html": html,
                "summary": summary,
                "publish_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        diaries.save(diary)
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
        ).to_xml()
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
        return db.diaries.find(limit=15).skip((int(page)-1)*15).sort('publish_time', -1)

    @staticmethod
    def up_to_upyun(data):
        img_data = data.get('body')
        img_name = data.get('filename').encode("utf-8")

        bucket = conf['upyun_bucket']
        admin = conf['upyun_admin']
        password = conf['upyun_password']

        u = UpYun(bucket, admin, password)
        u.setApiDomain('v0.api.upyun.com')
        #TODO u.setContentMD5(md5file(data))

        # save file
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")
        target = '/diary/%s/%s/%s/%s' % (year, month, day, img_name)
        a = u.writeFile(str(target) , img_data, True)
        url = conf['upyun_url'] + str(target)
        return url
