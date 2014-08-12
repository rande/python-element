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