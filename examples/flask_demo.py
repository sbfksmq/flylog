# -*- coding: utf-8 -*-
from flask import Flask

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

    'filters': {
    },

    'handlers': {
        'flylog': {
            'level': 'CRITICAL',
            'class': 'flylog.FlyLogHandler',
            'formatter': 'standard',
            'source': u'demo测试',
            'role_list': ['default', 'pm'],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },

    'loggers': {
        'default': {
            'handlers': ['console', 'flylog'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}


app = Flask(__name__)
app.config.from_object(__name__)


def configure_logging(app):
    import copy
    import logging.config

    LOGGING = copy.deepcopy(app.config['LOGGING'])
    LOGGING['loggers'][app.logger.name] = LOGGING['loggers']['default']
    logging.config.dictConfig(LOGGING)

@app.route('/')
def index():
    app.logger.debug('')
    app.logger.fatal(u'wo试试')
    app.logger.debug('')

    return 'ok'

if __name__ == '__main__':
    configure_logging(app)
    app.run(debug=True)
