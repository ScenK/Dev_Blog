#!/usr/local/bin/python
#coding=utf-8

from Config.config import config as conf 

db = conf.site_config()['db']

class Kid(object):
    def __init__():
        pass

    @staticmethod
    def kid():
        kid = db.kid.find_and_modify(update={"$inc":{"k":1}}, new=True).get("k")
        return kid

