# -*- coding: utf-8 -*-

import json
from logging.handlers import DatagramHandler

from . import constants


class FlyLogHandler(DatagramHandler):
    source = None

    def __init__(self, host=None, port=None, source=None):
        DatagramHandler.__init__(self,
                                 host or constants.FLY_LOG_AGENT_HOST,
                                 port or constants.FLY_LOG_AGENT_PORT)
        self.source = source

    def send(self, s):
        send_data = json.dumps(dict(source=self.source, content=s))

        return DatagramHandler.send(self, send_data)
