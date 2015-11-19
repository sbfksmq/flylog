# -*- coding: utf-8 -*-

# 通知方式
NOTIFY_TYPE_MAIL = 1
NOTIFY_TYPE_PUSH = 1 << 1

NOTIFY_TYPE = NOTIFY_TYPE_PUSH


# 邮件相关
import smtplib

MAIL_SENDER_LIST = [
    dict(
        host='smtp.qq.com',
        port=smtplib.SMTP_PORT,  # smtplib.SMTP_SSL_PORT
        username='xxx@qq.com',
        password='xxxx',
        sender='xxx@qq.com',
        use_ssl=False,
        use_tls=False,
    ),
]

MAIL_RECEIVER_LIST = dict(
    default=['fx@qq.com'],
    pdm=['f@qq.com']
)


# push相关
PUSH_APP_KEY = ''
PUSH_APP_SECRET = ''
