# -*- coding: utf-8 -*-
import smtplib

BACKENDS = {
    'mail': {
        'class': 'flylog.agent.backends.mail.MailBackend',
        'init_data': {
            'sender_list': [
                {
                    'host': 'smtp.qq.com',
                    'port': smtplib.SMTP_PORT,  # smtplib.SMTP_SSL_PORT
                    'username': 'xxx@qq.com',
                    'password': 'xxxx',
                    'sender': 'xxx@qq.com',
                    'use_ssl': False,
                    'use_tls': False,
                },
            ]
        },
    },
    'ding': {
        'class': 'flylog.agent.backends.ding.DingBackend',
        'init_data': {
            'corp_id': '',
            'corp_secret': '',
            'agent_id': '',
        }
    }
}

ROLES = {
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
            }
        },
    ]
}


# for logging

import logging

LOG_FORMAT = '\n'.join((
    '/' + '-' * 80,
    '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(filename)s:%(lineno)d %(funcName)s]:',
    '%(message)s',
    '-' * 80 + '/',
))

logger = logging.getLogger('flylog')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
