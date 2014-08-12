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
import os

class StaticHandler(element.node.NodeHandler):
    def __init__(self, base_dir, templating):
        self.base_dir = base_dir
        self.templating = templating

    def get_defaults(self, node):
        return {}

    def get_name(self):
        return 'Static'

    def execute(self, request_handler, context):
        if not context.mode or context.mode == 'raw':
            file = os.path.realpath(context.node.file)

            if file[:len(self.base_dir)] != self.base_dir:
                request_handler.set_status(404)

            request_handler.send_file(file)

        if context.mode == "preview":
            params = {
                'context': context
            }

            self.render(request_handler, self.templating, 'element.plugins.static:preview.html', params)
