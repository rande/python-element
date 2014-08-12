import ioc
import os
from element.plugins.livestats.handler import SystemWebSocket

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        websocket = config.get_dict('websocket', {
            'access':  'ws://localhost:5000/websocket/system',
            'handler': '/websocket/system'
        })

        container_builder.parameters.set('element.plugins.livestats.websocket.access', websocket['access'])
        container_builder.parameters.set('element.plugins.livestats.websocket.handler', websocket['handler'])

    def post_build(self, container_builder, container):
        self.container = container

        self.container.get('logger').info("livestats: Attach listener")
        container.get('ioc.extra.event_dispatcher').add_listener('ioc.extra.tornado.start', self.configure_tornado)

    def configure_tornado(self, event):
        logger = self.container.get('logger')
        logger.info("livestats: add SystemWebSocket handler")

        event.get('application').add_handlers(".*$", [(
            self.container.parameters.get('element.plugins.livestats.websocket.handler'),
            SystemWebSocket,
            {'logger': logger}
        )])
