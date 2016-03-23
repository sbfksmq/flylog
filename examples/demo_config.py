# -*- coding: utf-8 -*-
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


BACKEND_LIST = {
    'mail': {
        'class': 'flylog.backends.MailBackend',
        'params': {
            'host': 'smtp.qq.com',
            'port': smtplib.SMTP_PORT,  # smtplib.SMTP_SSL_PORT
            'username': 'xxx@qq.com',
            'password': 'xxxx',
            'sender': 'xxx@qq.com',
            'use_ssl': False,
            'use_tls': False,
        },
    },
    'ding': {
        'class': 'flylog.backends.DingBackend',
        'params': {
            'corp_id': '',
            'corp_secret': '',
        }
    }
}

ROLE_LIST = {
    'default': [
        {
            'backend': 'mail',
            'params': {
                'receiver_list': ['x@qq.com'],
            }
        },
        {
            'backend': 'ding',
            'params': {
                'user_list': ['1'],
                'party_list': ['1'],
                'agent_id': '',
            }
        }
    ]
}