# -*- coding: utf-8 -*-
import requests
from ..log import logger


class DingRobot(object):

    def __init__(self, web_hook_list):
        self.web_hook_list = web_hook_list

    def emit(self, title, content, user_list=None):
        """
        发送
        """
        full_content = '\n\n'.join([title, content])
        headers = {'Content-Type': 'application/json'}
        data = str({"msgtype": "text", "text": {"content": full_content}})
        logger.error('trace ding robot data: %s, headers: %s, web_hook: %s', data, headers, self.web_hook_list)
        for web_hook in self.web_hook_list:
            ret = requests.post(web_hook, data=data, headers=headers)
            logger.error('trace ding robot ret: %s', ret)
        return True
