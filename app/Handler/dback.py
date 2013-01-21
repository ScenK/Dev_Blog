#!/usr/local/bin/python
#coding=utf-8

import tornado.web
from lib.kid import Kid
from douban_client import DoubanClient
from Model.diaries import Diary
from Model.accounts import Account
from Config.config import config as conf 

conf = conf.site_config()

class DbackHandler(tornado.web.RequestHandler):
    def get(self, *args):

        KEY = '08e0dfb50c90b0991aa29f1f25b211cb'
        SECRET = '378ed0dadf96de47'
        CALLBACK = conf['url']+'/dback'
        SCOPE = 'douban_basic_common,community_basic_user,community_basic_note'

        client = DoubanClient(KEY, SECRET, CALLBACK, SCOPE)
        code = self.get_argument('code')

        if code:
            client.auth_with_code(code) 
            auth = client.user.me
            if auth:
                accounts = conf['db'].accounts
                account = {
                        "_id": Kid.kid(),
                        "id": auth.get('id'),
                        "name": auth.get('name'),
                        "avatar": auth.get('avatar'),
                        "loc_name": auth.get('loc_name'),
                        "desc": auth.get('desc')
                        }

                try:
                    exist = Account.get_by_id(auth.get('id'))

                    if exist is None:
                        accounts.save(account)
                    else:
                        accounts.update({'id': auth.get('id')}, {'$set': account})

                except Exception as e:
                    print str(e)

                diary = client.note.list(auth.get('id'), 0, 20)
                diaries = conf['db'].diaries
                diary_notes = diary.get('notes')
                for i in diary_notes:
                    
                    # re-summary content from douban
                    summary = i.get('content')[0:80] + '...'
                    
                    diary = {
                            "_id": Kid.kid(),
                            "update_time": i.get('update_time'),
                            "publish_time": i.get('publish_time'),
                            "photos": i.get('photos'),
                            "comments_count": i.get('comments_count'),
                            "liked_count": i.get('liked_count'),
                            "recs_count": i.get('recs_count'),
                            "id": i.get('id'),
                            "alt": i.get('alt'),
                            "can_reply": i.get('can_reply'),
                            "title": i.get('title'),
                            "privacy": i.get('privacy'),
                            "summary": summary,
                            "content": client.note.get(i.get('id'), format='html_full').get('content')
                            }
                    try:
                        exist = Diary.get_by_id(i.get('id'))

                        if exist is None:
                            diaries.save(diary)
                        else:
                            diaries.update({'id': i.get('id')}, {'$set': diary})

                    except Exception as e:
                        print str(e)

                self.redirect('/')
        else:
            print 'douban_callback code missing'


