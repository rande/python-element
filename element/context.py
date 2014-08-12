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

from node import NodeContext

class ContextCreator(object):
    def __init__(self, event_dispatcher, defaults=None):
        self.event_dispatcher = event_dispatcher
        self.defaults = defaults or {
            'base_template': 'element:base.html',
        }
        
    def build(self, node, handler, defaults=None):
        settings = {}

        settings.update(self.defaults)
        settings.update(handler.get_defaults(node))
        settings.update(node.data)
        settings.update(defaults or {})

        if not settings['base_template']:
            settings['base_template'] = 'element:empty.html'

        context = NodeContext(node, settings)

        self.event_dispatcher.dispatch('element.node.context.load', {
            'context': context
        })

        return context