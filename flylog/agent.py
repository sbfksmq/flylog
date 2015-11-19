#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用来作为接受log传递的agent
通过udp通道。
"""

import json
import logging
import logging.config
import SocketServer
import copy
import random

logger = logging.getLogger('flylog')


def send_mail(host, port, sender, receivers, subject, content,
             content_type='plain', encoding='utf-8',
             username=None, password=None, use_ssl=False, use_tls=False, debuglevel=0
             ):
    """
    发送邮件
    content_type: plain / html
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    from email.utils import formatdate

    mail_msg = MIMEText(content, content_type, encoding)
    mail_msg['Subject'] = Header(subject, encoding)
    mail_msg['From'] = sender
    mail_msg['To'] = ', '.join(receivers)
    mail_msg['Date'] = formatdate()

    if use_ssl:
        mail_client = smtplib.SMTP_SSL(host, port)
    else:
        mail_client = smtplib.SMTP(host, port)

    mail_client.set_debuglevel(debuglevel)

    if use_tls:
        mail_client.starttls()

    if username and password:
        mail_client.login(username, password)

    # 发邮件
    mail_client.sendmail(sender, receivers, mail_msg.as_string())
    mail_client.quit()


def send_push(app_key, app_secret, title, content, tags):
    """
    发送push
    因为到了本地之后要缓存起来，所以只能走自定义消息
    """

    import jpush

    _jpush = jpush.JPush(app_key, app_secret)
    push = _jpush.create_push()
    push.audience = jpush.audience(
        jpush.tag(*tags),
    )
    # 自定义消息，ios只能在前台收到，所以要用通知
    push.notification = jpush.notification(
        ios=jpush.ios(title, extras=dict(
            content=content,
        )),
        android=jpush.android(title, extras=dict(
            content=content
        ))
    )
    push.platform = jpush.all_

    push.platform = jpush.all_
    # 如果不设置，默认发送到生产环境
    # 设置为False，代表发送到开发环境。
    push.options = {"apns_production": False}
    try:
        push.send()
        return True
    except Exception, e:
        # logger.error(u"jpush failed, tags: %s\ncontent: %s", tags, content, exc_info=True)
        return False


class FlyLogAgent(object):
    debug = False

    def __init__(self, config=None, debug=None):
        self.config = config
        if debug is not None:
            self.debug = debug

    def _handle_message_by_mail(self, recv_dict):
        """
        通过邮件处理消息
        """
        role_list = recv_dict.get('role_list') or ('default',)
        receiver_list = []
        for role, one_receiver_list in self.config.MAIL_RECEIVER_LIST.items():
            if role in role_list:
                receiver_list.extend(one_receiver_list)

        receiver_list = list(set(receiver_list))

        if not receiver_list:
            # 如果没有接收者，就直接返回了
            return

        sender_list = list(copy.deepcopy(self.config.MAIL_SENDER_LIST))

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
                send_mail(**mail_values)
            except:
                logger.error("exc occur. mail_values: %s", mail_values, exc_info=True)
            else:
                # 如果成功发送
                break

    def _handle_message_by_push(self, recv_dict):
        """
        通过push处理消息
        """
        role_list = recv_dict.get('role_list') or ('default',)
        # content太长显示不了
        send_push(self.config.PUSH_APP_KEY, self.config.PUSH_APP_SECRET, recv_dict.get('title'), role_list)

    def handle_message(self, message, address):
        recv_dict = json.loads(message)

        if self.config.NOTIFY_TYPE & self.config.NOTIFY_TYPE_MAIL:
            self._handle_message_by_mail(recv_dict)

        if self.config.NOTIFY_TYPE & self.config.NOTIFY_TYPE_PUSH:
            self._handle_message_by_push(recv_dict)

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
