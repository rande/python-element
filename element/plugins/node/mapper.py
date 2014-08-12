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

class Meta(object):
    def __init__(self, klass, node_type):
        self.klass = klass
        self.node_type = node_type
        self.methods = {}

class Manager(object):
    def __init__(self):
        self.collection = MetaCollection

class MetaCollection(object):
    def __init__(self):
        self.metas = {}

    def add(self, meta):
        self.metas[meta.node_type] = meta

class MetaListener(object):
    def __init__(self, collection):
        self.collection = collection

    def on_load(self, node):
        if node.type not in self.collection.metas:
            return

        node.__class__ = self.collection.metas[node.type].klass

    def on_node_load(self, event):
        self.on_load(event.get('node'))

    def on_nodes_load(self, event):
        for node in event.get('nodes'):
            self.on_load(node)