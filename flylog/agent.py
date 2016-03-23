#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用来作为接受log传递的agent
通过udp通道。
"""

import json
import SocketServer
import copy
import random
from log import logger


class FlyLogAgent(object):
    debug = False

    def __init__(self, config=None, debug=None):
        self.config = config
        if debug is not None:
            self.debug = debug

    def handle_message(self, message, address):
        recv_dict = json.loads(message)

        role_list = recv_dict.get('role_list') or ('default',)

        while sender_list:
            # 只要还有sender
            # 保证随机
            random.shuffle(sender_list)

            # 取出最后一个
            mail_values = sender_list.pop()
            mail_values['receivers'] = receiver_list
            mail_values['subject'] = u'[%s]Attention!' % recv_dict.get('source')
            mail_values['content'] = recv_dict.get('content')

            try:
                sendmail(**mail_values)
            except:
                logger.error("exc occur. mail_values: %s", mail_values, exc_info=True)
            else:
                # 如果成功发送
                break

    def run(self, host, port):
        class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
            def handle(sub_self):
                message = sub_self.request[0]
                try:
                    self.handle_message(message, sub_self.client_address)
                except:
                    logger.error('exc occur.', exc_info=True)

        server = SocketServer.ThreadingUDPServer((host, port), ThreadedUDPRequestHandler)

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        except:
            logger.error('exc occur.', exc_info=True)
