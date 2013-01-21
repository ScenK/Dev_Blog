#!/usr/local/bin/python
#coding=utf-8

from Config.config import config as conf 

db = conf.site_config()['db']

class Account(object):
    def __init__(self, user):
       self.user = user

    @staticmethod
    def get():
        accounts = db.accounts
        profile = accounts.find_one()
        return profile

    @staticmethod
    def get_by_id(id):
        accounts = db.accounts
        exist = accounts.find_one({'id': id})
        if exist is None:
            return None
        else:
            return 'exist'

       

