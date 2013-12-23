# -*- coding: utf-8 -*-
import smtplib

MAIL_SERVER = 'smtp.qq.com'
MAIL_USERNAME = 'xxx@qq.com'
MAIL_PASSWORD = 'xxxxxxx'
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_SENDER = 'xxx@qq.com'
MAIL_RECEIVER_LIST = ['xxx@qq.com']
if MAIL_USE_SSL:
    MAIL_PORT = smtplib.SMTP_SSL_PORT
else:
    MAIL_PORT = smtplib.SMTP_PORT
