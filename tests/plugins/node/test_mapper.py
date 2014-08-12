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

import unittest
from element.plugins.node.mapper import Manager, Meta, MetaCollection, MetaListener
from element.node import Node
from ioc.event import Event
import datetime

class NodeImage(Node):
    pass

class MapperTest(unittest.TestCase):
    def test_meta(self):
        m = Meta(Node, 'mytype')

        self.assertEquals('mytype', m.node_type)

    def test_change_class(self):
        c = MetaCollection()
        c.add(Meta(NodeImage, 'image'))
        l = MetaListener(c)

        # valid type
        event = Event({'node': Node(None, {'type': 'image'})})
        l.on_node_load(event)
        self.assertEquals(event.get('node').__class__, NodeImage)

        # invalid type
        event = Event({'node': Node(None, {'type': 'fake'})})
        l.on_node_load(event)
        self.assertEquals(event.get('node').__class__, Node)


    def test_add_method(self):

        class Manager(object):
            def get_uuid(self, node, *args, **kwargs):
                return "%s: %s" % (node.uuid, kwargs)

        def wrapper(function):
            return lambda node, *args, **kwargs: function(node, *args, **kwargs)

        def my_method(node):
            return "hello world! ~ uuid: %s" % node.uuid

        n = Node("550e8400-e29b-41d4-a716-446655440000")
        n.methods['my_method'] = my_method

        m = Manager()

        self.assertEquals("hello world! ~ uuid: 550e8400-e29b-41d4-a716-446655440000", n.my_method())

        setattr(NodeImage, 'my_method', my_method)
        setattr(NodeImage, 'class_method', lambda node, *args, **kwargs: m.get_uuid(node, *args, **kwargs))
        setattr(NodeImage, 'wrapper_method', wrapper(m.get_uuid))

        n = NodeImage("550e8400-e29b-41d4-a716-446655440000", {
            'updated_at': datetime.datetime(2014, 4, 1, 19, 3, 39, 720519),
            'created_at': datetime.datetime(2014, 4, 1, 19, 3, 39, 720519),
        })

        self.assertEquals("hello world! ~ uuid: 550e8400-e29b-41d4-a716-446655440000", n.my_method())
        self.assertEquals("550e8400-e29b-41d4-a716-446655440000: {'foo': 'bar'}", n.class_method(foo='bar'))
        self.assertEquals("550e8400-e29b-41d4-a716-446655440000: {'foo': 'bar'}", n.wrapper_method(foo='bar'))

        self.assertEquals(n.__dict__,  {
            'created_at': datetime.datetime(2014, 4, 1, 19, 3, 39, 720519),
            'current': True,
            'data': {},
            'deleted': False,
            'enabled': True,
            'id': None,
            'manager': None,
            'methods': {},
            'path': None,
            'revision': 1,
            'set': None,
            'set_uuid': None,
            'status': 0,
            'type': None,
            'updated_at': datetime.datetime(2014, 4, 1, 19, 3, 39, 720519),
            'uuid': '550e8400-e29b-41d4-a716-446655440000',
            'version': 1,
            'weight': 0
        })