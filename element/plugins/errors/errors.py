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

class ErrorListener(object):
    def __init__(self, node_manager, renderer):
        self.node_manager = node_manager
        self.renderer = renderer

    def handle_400_error(self, event):
        return self.handle('errors/40x', event)

    def handle_500_error(self, event):
        return self.handle('errors/50x', event)

    def handle(self, path, event):
        node = self.node_manager.get_node(path)

        if not node or not event.has('request_handler'):
            return

        self.renderer.render(event.get('request_handler'), node)