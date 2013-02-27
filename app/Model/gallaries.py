#!/usr/local/bin/python
#coding=utf-8

from Config.config import config as conf 
import datetime
from lib.kid import Kid
from lib.upyun import UpYun,md5,md5file

db = conf.site_config()['db']
conf = conf.site_config()

class Gallary(object):
    def __init__(self):
       pass

    @staticmethod
    def get_detail(_id):
        return db.gallaries.find_one({'_id': int(_id)})

    @staticmethod
    def get_all():
        return db.gallaries.find().sort('publish_time', -1)

    @staticmethod
    def add(title, desc):
        gallaries = db.gallaries

        galllary = {
                    "_id": Kid.kid(),
                    "title": title,
                    "photo_count": 0,
                    "description": desc,
                    "publish_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
        gallaries.save(galllary)
        return

    @staticmethod
    def del_adbum(_id):
        return db.gallaries.remove({'_id': int(_id)})

    @staticmethod
    def up_to_upyun(collection, data):
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
        target = '/%s/%s/%s/%s/%s' % (collection, year, month, day, img_name)
        a = u.writeFile(str(target) , img_data, True)
        url = conf['upyun_url'] + str(target)
        return url

    @staticmethod
    def save_photo(gid, url, title):
        content = {
                "_id": Kid.kid(),
                "title": title,
                "gid": int(gid),
                "url": url,
                "publish_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

        # save gallary index
        index = Gallary.get_detail(gid).get('index')
        if index is None:
            db.gallaries.update({'_id': int(gid)}, {'$set': {'index': url}})

        #i update gallary detail
        db.gallaries.update({'_id': int(gid)}, {'$inc': {'photo_count': 1}, 
                                         '$push': {'content': content}})
        return

    @staticmethod
    def del_photo(gid, _id):
        return db.gallaries.update({'_id': int(gid)}, {'$pull': {'content': {'_id': int(_id)}} 
                                            ,'$inc': {'photo_count': -1}})
