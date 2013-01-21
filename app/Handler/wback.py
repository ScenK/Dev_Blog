#!/usr/local/bin/python
#coding=utf-8

import tornado.web
from lib.kid import Kid
from weibo import APIClient
from Model.accounts import Account
from Config.config import config as conf

conf = conf.site_config()

class WbackHandler(tornado.web.RequestHandler):
    def get(self, *args):
        # OAth2 for sina_weibo
        APP_KEY =  conf['weibo_app_key']
        APP_SECRET = conf['weibo_app_secret']
        CALLBACK_URL = conf['url'] + '/wback'

        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

        code = self.get_argument('code')
        r = client.request_access_token(code)
        access_token = r.access_token
        expires_in = r.expires_in
        client.set_access_token(access_token, expires_in)

        _id = client.account.get_uid.get().get('uid')
        auth = client.users.show.get(uid=_id)
        
        if auth:
            accounts = conf['db'].accounts
            account = {
                    "_id": Kid.kid(),
                    "id": auth.get('id'),
                    "name": auth.get('screen_name'),
                    "avatar": auth.get('profile_image_url'),
                    "loc_name": auth.get('location'),
                    "desc": auth.get('description'),
                    }

            try:
                exist = Account.get_by_id(auth.get('id'))

                if exist is None:
                    accounts.save(account)
                else:
                    accounts.update({'id': int(auth.get('id'))}, {'$set': account})

                    self.set_secure_cookie("user", account.get('name'))
            except Exception as e:
                print str(e)

            self.redirect('/')
