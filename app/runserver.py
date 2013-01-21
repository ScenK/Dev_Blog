#!/usr/local/bin/python
#coding=utf-8
#author: He.Kang@dev-engine.com

import sys
sys.path.append('../lib/')

import tornado.options
from tornado.httpserver import HTTPServer

from application import application

from Config.config import config

config = config.site_config()

PORT = config['port']

def main():
    tornado.options.parse_command_line()
    application.listen(PORT)
    print 'Dev server is running as http://127.0.0.1:%s/' % PORT
    print 'Quit the server with CONTROL-C'
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()



