# -*- coding: utf-8 -*-
import smtplib

BACKENDS = {
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
        }
    },

}

FILTER_SETTING = {
    # 为了避免发送重复的日志  通过 日志内容的md5值为key记录重复次数
    'resend_times': 2,
    'redis_setting': {
        'db_name': 'app_default',
        'host': '10.0.0.72',
        'port': '6379',
        'password': '',
        'db': '3',
        'auto_expire_time': 24 * 60 * 60,
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
