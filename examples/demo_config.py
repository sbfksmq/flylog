# -*- coding: utf-8 -*-
import smtplib

BACKENDS = {
    'mail': {
        'class': 'flylog.server.backends.mail.MailBackend',
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
        'class': 'flylog.server.backends.ding.DingBackend',
        'init_data': {
            'corp_id': '',
            'corp_secret': '',
            'agent_id': '',
        }
    },

    'robot': {
        'class': 'flylog.server.backends.robot.DingRobot',
        'init_data': {
            'web_hook_service_map': {
                'https://oapi.dingtalk.com/robot/send?access_token=5ccc235d16a06cfb097a24d5bcc4a8302593af52bb702250859ef4c6a5d07e96': [
                'g_p_h_mtt', 'g_p_mtt2', 'g_p_mtt'],
            },
            'resend_times': 2,
            'redis_setting:': {
                'db_name': 'db_name',
                'host': '127.0.0.1',
                'port': '22',
                'password': '123456',
                'db': '13',
                'auto_expire': 3*24*24,
            },
        }
    },

    'sendcloud': {
        'class': 'flylog.server.backends.sendcloud.SendCloudBackend',
        'init_data': {
            'api_user': '',
            'api_key': '',
            'sender': '',
        }
    },
}

FILTER_SETTING = {
    # 为了避免发送重复的日志  通过 日志内容的md5值为key记录重复次数
    'resend_times': 2,
    'redis_setting': {
        'db_name': 'app_default',
        'host': '127.0.0.1',
        'port': '6379',
        'password': '',
        'db': '2',
        'auto_expire': 3 * 24 * 24,
    }
}


ROLES = {
    'default': [
        {
            'backend': 'ding',
            'params': {
                'user_list': ['1'],
                'party_list': ['1'],
            },
        },
        {
            'backend': 'robot',
            'params': {
            }
        },
    ]
}


LOG_FORMAT = '\n'.join((
    '/' + '-' * 80,
    '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(filename)s:%(lineno)d %(funcName)s]:',
    '%(message)s',
    '-' * 80 + '/',
))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'standard': {
            'format': LOG_FORMAT,
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },

    'loggers': {
        'flylog': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False
        },
    }
}
