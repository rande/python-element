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

class GalleryHandler(element.node.NodeHandler):
    def __init__(self, templating):
        self.templating = templating

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.media:gallery.html'
        }

    def get_name(self):
        return 'Media Gallery'

    def execute(self, request_handler, context):
        medias = context.node.medias()

        params = {
            'context': context,
            'medias':  medias,
            'lines': [
                [x for x in range(len(medias)) if x - 0 == 0 or ((x - 0) % 4 == 0)],
                [x for x in range(len(medias)) if x - 1 == 0 or ((x - 1) % 4 == 0)],
                [x for x in range(len(medias)) if x - 2 == 0 or ((x - 2) % 4 == 0)],
                [x for x in range(len(medias)) if x - 3 == 0 or ((x - 3) % 4 == 0)],
            ],
        }
        
        self.render(request_handler, self.templating, context.settings['template'], params)

class MediaHandler(element.node.NodeHandler):

    def __init__(self, templating):
        self.templating = templating

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.media:media.html'
        }

    def get_name(self):
        return 'Media'

    def execute(self, request_handler, context):

        params = {
            'context': context,
        }

        self.render(request_handler, self.templating, context.settings['template'], params)