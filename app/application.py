#!/usr/local/bin/python
#conding: utf-8
#author: He.Kang@dev-engine.com

from urls import urls

import tornado.database
import tornado.web
import os
from Config.config import config

config = config.site_config()

SETTINGS = dict(
    template_path = os.path.join(os.path.dirname(__file__), "View"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret = config['cookie'],
    db = config['db'],
    title = config['title'],
    url = config['url'],
    keywords = config['keywords'],
    desc = config['description'],
    login_url = "/login",
    autoescape = None,
    xsrf_cookies = True,
    debug = config['debug'],
    analytics = config['analytics']
)
application = tornado.web.Application(
                    handlers = urls,
                    **SETTINGS
)
