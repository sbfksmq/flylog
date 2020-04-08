# -*- coding: utf-8 -*-
import json
import requests
from ..log import logger


class DingRobot(object):

    RET_OK = 0

    def __init__(self, web_hook_service_map):
        self.web_hook_service_map = web_hook_service_map

    def emit(self, title, content, service_name=None):

        logger.info('trace data title: %s, content: %s, service_name: %s, map: %s',
                    title, content, service_name, self.web_hook_service_map)

        full_content = '\n\n'.join([title, content])
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({"msgtype": "text", "text": {"content": full_content}})

        res_list = []
        logger.info('trace data map: %s', self.web_hook_service_map)
        for web_hook, service_list in self.web_hook_service_map.items():
            logger.info('trace data web_hook1 : %s, service_list: %s', web_hook, service_list)
            if service_name in service_list:
                rsp = requests.post(web_hook, data=data, headers=headers).json()
                logger.info('trace data rsp: %s', rsp)
                res_list.append(rsp['errcode'] in [self.RET_OK, ])
            logger.info('trace data web_hook2 : %s, service_list: %s', web_hook, service_list)
        return False not in res_list
