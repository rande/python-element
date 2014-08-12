#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from tornado.websocket import WebSocketHandler

import tornado
import psutil
import json

class SystemWebSocket(WebSocketHandler):
    def initialize(self, logger=None):
        self.logger = logger

    def open(self):
        self.logger.debug("SystemWebSocket: Open")

        self.pref = tornado.ioloop.PeriodicCallback(self.tick, 1000)
        self.pref.start()

    def tick(self):
        swap = psutil.swap_memory()
        memory = psutil.virtual_memory()

        message = json.dumps({
            'host1': {
                'memory': {
                    'swap_memory' : {
                        'name': 'Swap',
                        'min': 0,
                        'max': swap.total / (1024*10124),
                        'value': swap.used / (1024*10124),
                    },
                    'virtual_memory': {
                        'name': 'Virual Memory',
                        'min': 0,
                        'max': memory.total / (1024*1024),
                        'value': memory.used / (1024*1024),
                    }
                },
                'cpu': {
                    'min': 0,
                    'max': 100,
                    'value': psutil.cpu_percent()
                }
            }
        })

        self.logger.debug("SystemWebSocket: tick=%s" % message)

        self.write_message(message)

    def on_message(self, message):
        self.logger.debug("SystemWebSocket: call dispatcher %s" % message)

    def on_close(self):
        self.logger.debug("SystemWebSocket: Close")
        self.pref.stop()