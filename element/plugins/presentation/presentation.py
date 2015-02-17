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

class PresentationHandler(element.node.NodeHandler):
    def __init__(self, formatter):
        self.formatter = formatter

    def get_name(self):
        return 'Presentation'

    def get_defaults(self, node):

        if node.type == 'presentation.reveal':
            return {
                'base_template': 'element.plugins.presentation:reveal_base.html',
                'template':      'element.plugins.presentation:reveal_node.html',
                'abstract': False
            }

        if node.type == 'presentation.raw':
            return {
                'template': 'element.plugins.presentation:raw.html',
                'abstract': False
            }

        if node.type == 'presentation.shower':
            return {
                'theme':         'ribbon',
                'base_template': 'element.plugins.presentation:shower_base.html',
                'template':      'element.plugins.presentation:shower_node.html',
                'abstract':      False
            }

        if node.type == 'presentation.slideshare':

            width = node.width or 597
            height = 486

            if not node.height:
                height = (width * 3) / 4

            return {
                'template': 'element.plugins.presentation:slideshare.html',
                'width': width,
                'height': height,
                'abstract': False
            }

        return {}

    def execute(self, request_handler, context):
        return 200, context.settings['template'], {
            'context': context,
        }
