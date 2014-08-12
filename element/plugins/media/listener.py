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

class MediaNode(Node):
    pass

class MediaGalleryNode(Node):
    pass

class ProxyStaticMethod(object):
    def __init__(self, types):
        self.types = types

    def is_image(self, node):
        return node.extension.lower() in self.types['image']

    def is_video(self, node):
        return node.extension.lower() in self.types['video']

    def is_document(self, node):
        return node.extension.lower() in self.types['document']

class ProxyMediasMethod(object):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def __call__(self, node, *args, **kwargs):
        """
        Return the list of media for the related media
        """
        return self.node_manager.get_nodes(**{
            'type': 'element.static',
            'path': node.path
        })

class MediaListener(object):
    def __init__(self, proxy_media_method, proxy_static_method):
        self.proxy_media_method = proxy_media_method
        self.proxy_static_method = proxy_static_method

    def register(self, event):

        collection = event.get('meta_collection')

        collection.add(Meta(MediaGalleryNode, 'media.gallery'))
        collection.add(Meta(MediaNode, 'element.static'))

    def define(self, event):

        collection = event.get('meta_collection')

        collection.metas['media.gallery'].methods['medias'] = self.proxy_media_method

        collection.metas['element.static'].methods['is_image'] = self.proxy_static_method.is_image
        collection.metas['element.static'].methods['is_video'] = self.proxy_static_method.is_video
        collection.metas['element.static'].methods['is_document'] = self.proxy_static_method.is_document


    def normalize(self, event):
        if event.has('node'):
            nodes = [event.get('node')]
        else:
            nodes = event.get('nodes')

        for node in nodes:
            # normalize required parameters
            if not node.parameters:
                node.parameters = {}

            if 'types' not in node.parameters:
                node.parameters['types'] = ['png', 'jpg', 'gif']

            if 'format' not in node.parameters:
                node.parameters['format'] = 'small'