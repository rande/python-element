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

import element.node

class ActionView(object):
    def __init__(self, rendered, event_dispatcher):
        self.rendered = rendered
        self.event_dispatcher = event_dispatcher

    def dispatch(self, request_handler, *args, **kwargs):
        if '_controller' not in kwargs:
            return

        serviceId, method = kwargs['_controller'].split(":")

        del kwargs['_controller']

        parameters = request_handler.request.query_arguments.copy()
        parameters.update(kwargs)

        node = element.node.Node('action://%s' % serviceId, {
            'type': 'action.node',
            'serviceId': serviceId,
            'method': method,
            'kwargs': parameters,
            'request': request_handler.request
        })

        event = self.event_dispatcher.dispatch('element.node.load.success', {
            'node': node
        })

        return self.rendered.render(request_handler, event.get('node'))
