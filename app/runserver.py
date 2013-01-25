#!/usr/local/bin/python
#coding=utf-8
#author: He.Kang@dev-engine.com

import sys

import tornado.web
from tornado.options import define, options, logging
from tornado.httpserver import HTTPServer
from application import application

define("port", default=8888, help="run on the given port", type=int)

def main():
    tornado.options.parse_command_line()
    logging.info("Starting Tornado web server on http://127.0.0.1:%s" % options.port)
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    print 'Quit the server with CONTROL-C'

if __name__ == "__main__":
    main()
