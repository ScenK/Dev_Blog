#!/usr/local/bin/python
#conding: utf-8

import re
from fabric.api import *
import datetime
from Config.config import config as conf

conf = conf.site_config()

@task
def deploy():
    execute(lessc)
    execute(compress)

@task
def test():
    local("python ./runserver.py --port=8000")

@task
def build():
    admins = conf['db'].admins
    kid = conf['db'].kid
    admin = {'user': conf['username'], 'password': conf['password'], 'site_start':datetime.datetime.now().strftime("%Y-%m-%d")}
    admins.save(admin)
    print "Default Admin add Success!"
    kid.save({'k': 0})
    print "Auto uuid add Success!"

@task
def compress():
    execute(compress_js)
    execute(compress_css)

@task
def compress_js():
    js_files = ['frontend', 'backend']

    local("rm -f static/js/*.min*.js")

    for f in js_files:
        local(
            'java -jar yuicompressor.jar --charset utf-8 --type js %s >> %s' %
            ('static/js/'+f+'.js', 'static/js/'+f+'.min.js'))

@task
def compress_css():
    css_files = ['frontend', 'backend', 'ie-style']

    local("rm -f static/css/*.min*.css")

    for f in css_files:
        local(
            'java -jar yuicompressor.jar --charset utf-8 --type css %s >> %s' %
            ('static/css/'+f+'.css', 'static/css/'+f+'.min.css'))

@task
def lessc():
    local("lessc static/less/frontend.less > static/css/frontend.css")
    local("lessc static/less/backend.less > static/css/backend.css")
    local("lessc static/less/ie-style.less > static/css/ie-style.css")


@task
def update():
    local("git pull")
    execute(deploy)

