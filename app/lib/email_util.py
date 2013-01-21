#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.Header import Header
from Config.config import config as conf

conf = conf.site_config()

def send_mail(receiver, title, content):
    sender = conf['smtp_user']
    password = conf['smtp_password']
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(title,"UTF-8")
    msg['From'] = sender
    msg['To'] = receiver
    part = MIMEText(content, 'html', _charset='UTF-8')
    msg.attach(part)

    server = smtplib.SMTP(conf['smtp_server'], conf['smtp_port'])
    server.starttls()
    server.login(sender,password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
