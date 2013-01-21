#!/usr/local/bin/python
#coding=utf-8

from Config.config import config as conf 

db = conf.site_config()['db']

class Admin(object):
    def __init__(self, user):
       self.user = user

    @staticmethod
    def find_by_username(user):
        admin = db.admins
        profile = admin.find_one({'user': user})
        return profile
