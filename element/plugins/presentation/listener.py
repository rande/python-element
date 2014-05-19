from element.node import Node
from element.plugins.node.mapper import Meta
import re

class Slide(object):
    def __init__(self, content, format="markdown"):
        self.content = content
        self.format = format

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

        for content in re.split('(\n|\r\n)----', self.content):
            if content.strip() == "":
                continue

            self._slides.append(Slide(content))


class PresentationListener(object):
    def register(self, event):
        collection = event.get('meta_collection')

        collection.add(Meta(PresentationNode, 'presentation.shower'))
