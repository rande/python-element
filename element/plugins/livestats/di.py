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
