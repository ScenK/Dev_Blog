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
    execute(compress_all_js)
    execute(compress_css)

@task
def compress_all_js():
    compress_js('frontend')
    compress_js('backend')

@task
def compress_js(debug_files):
    js_files = []

    target  = open('static/js/'+debug_files+'.js', "r")
    p = re.compile("document.*src=\'/(.*?)\'.*")
    for line in target:
        m = p.match(line)
        if m:
            js_files.append(m.group(1))
    target.close()

    local("rm -f static/js/%s.min*.js" % debug_files)

    compressed_file = "static/js/%s.min.js" % debug_files
    for f in js_files:
        local(
            'java -jar yuicompressor.jar --charset utf-8 --type js %s >> %s' %
            (f, compressed_file))

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
