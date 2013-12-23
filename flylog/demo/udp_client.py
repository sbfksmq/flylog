#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import json

address = ('127.0.0.1', 12000)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udp 也可以connect的
s.connect(address)

send_dict = dict(
    source=u'测试客户端',
    content=u'好像有异常',
)

s.send(json.dumps(send_dict) + '\n')
print 'sended'
s.close()

