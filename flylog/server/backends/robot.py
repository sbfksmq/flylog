# -*- coding: utf-8 -*-
import json
import requests

from ..log import logger
from ..redis_helper import FlylogMsgCache
from ..utils import TextHandlerPokio


class DingRobot(object):

    ERROR_CODE_KEYWORD = 310000
    RET_OK = 0

    def __init__(self, web_hook_list, redis_setting=None, resend_times=1):
        self.web_hook_list = web_hook_list
        self.resend_times = resend_times
        self.redis_setting = redis_setting

    def _is_reached_message_send_limit(self, content_md):
        return FlylogMsgCache(content_md, self.redis_setting).get_times() >= self.resend_times

    def emit(self, title, content):

        full_content = '\n\n'.join([title, content])
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({"msgtype": "text", "text": {"content": full_content}})

        logger.debug('trace debug redis_setting: %s', self.redis_setting)

        if self.redis_setting:
            content_md = TextHandlerPokio.handle(content)
            if not content_md:
                logger.error('file info invalid content info: %s', content)
                return False

            if self._is_reached_message_send_limit(content_md):
                logger.error('log info reached resend limit content: %s', content)
                return True

            FlylogMsgCache(content_md, self.redis_setting).set_times()

        res_list = []
        for web_hook in self.web_hook_list:
            rsp = requests.post(web_hook, data=data, headers=headers).json()
            res_list.append(rsp['errcode'] in [self.ERROR_CODE_KEYWORD, self.RET_OK])

        return False not in res_list
