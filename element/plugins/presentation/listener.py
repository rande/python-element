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

from element.node import Node
from element.plugins.node.mapper import Meta
import re
import markdown

class Slide(object):
    def __init__(self, content, meta, raw=Node):
        self.content = content
        self.meta = meta
        self.raw = raw

class PresentationNode(Node):
    def __init__(self, uuid=None, data=None):
        super(PresentationNode, self).__init__(uuid=uuid, data=data)
        self._slides = False

    def slides(self):
        if not self._slides:
            self.build_slides()

        return self._slides

    def build_slides(self):
        self._slides = []

        for raw in re.split('(\n|\r\n)----', self.content):
            raw = raw.strip()

            if raw == "":
                continue

            md = markdown.Markdown(extensions = ['tables', 'codehilite', 'fenced_code', 'meta'])
            content = md.convert(raw)

            for field in ['class', 'id', 'data-timing', 'data-state']:
                if field not in md.Meta:
                    md.Meta[field] = False
                else:
                    md.Meta[field] = " ".join(md.Meta[field])

            self._slides.append(Slide(content, md.Meta, raw))


class PresentationListener(object):
    def register(self, event):
        collection = event.get('meta_collection')

        collection.add(Meta(PresentationNode, 'presentation.shower'))
        collection.add(Meta(PresentationNode, 'presentation.reveal'))
