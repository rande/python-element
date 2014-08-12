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
import ioc.event
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from element.manager.mongo import MongoManager, InvalidDataFormat
from pymongo.errors import DuplicateKeyError
from element.manager import get_uuid

class MongoManagerTest(unittest.TestCase):
    def setUp(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.manager = MongoManager(self.client, '_ci_python_element_test', '_ci_python_collection')
        self.manager.get_collection().remove()

        self.manager.get_collection().insert({
            "_id": ObjectId("507f1f77bcf86cd799439012"),
            "uuid": get_uuid('my-first-blog-post'),
            "author": "Mike",
            "text": "My first blog post!",
            "slug": "my-first-blog-post",
            "parent": None,
            "path": "/myfirst-blog-post",
            "tags": ["mongodb", "python", "pymongo"],
        })

    def test_retrieve(self):
        self.assertIsNone(self.manager.retrieve("ad"))
        self.assertIsNone(self.manager.retrieve("c875b4ea-9682-aeaf-2dec4c5e"))
        data = self.manager.retrieve("b875b4ea-9682-aeaf-2dec4c5e")
        self.assertIsNotNone(data)
        self.assertTrue("id" in data)

    def test_exists(self):
        self.assertFalse(self.manager.exists("c875b4ea-9682-aeaf-2dec4c5e"))
        self.assertTrue(self.manager.exists("b875b4ea-9682-aeaf-2dec4c5e"))

    def test_delete(self):
        self.assertEquals(1, self.manager.delete("b875b4ea-9682-aeaf-2dec4c5e"))
        self.assertEquals(0, self.manager.delete("b875b4ea-9682-aeaf-2dec4c5e"))

    def test_save_no_parent(self):
        with self.assertRaises(InvalidDataFormat):
            self.manager.save(None, {"type": "core.user", "name": "Thomas Rabaix"})

        data = self.manager.save(None, {"type": "core.user", "name": "Thomas Rabaix", "slug": "thomas-rabaix"})

        self.assertTrue("id" in data)
        self.assertTrue("uuid" in data)
        self.assertIsNotNone(data['uuid'])
        self.assertIsNotNone(data['id'])
        self.assertIsNone(data['parent'])
        self.assertEquals("/thomas-rabaix", data['path'])

    def test_save_with_parent_no_child(self):
        parent = self.manager.save(None, {"type": "core.node", "name": "articles", 'slug': 'articles'})

        self.assertEquals('/articles', parent['path'])

        child = self.manager.save(None, {"type": "core.post", "name": "Python Element", 'slug': 'python-element', 'parent': parent['uuid']})

        self.assertEquals('/articles/python-element', child['path'])

    def test_save_with_children(self):
        parent = self.manager.save(None, {"name": "articles", 'slug': 'articles', 'type': "core.node"})
        child = self.manager.save(None, {"name": "Python Element", 'slug': 'python-element', 'parent': parent['uuid'], 'type':  "core.post"})

        parent['slug'] = 'new-articles'

        parent = self.manager.save(parent['uuid'], parent)

        child = self.manager.retrieve(child['uuid'])

        self.assertIsNotNone(child)

        self.assertEquals("/new-articles/python-element", child['path'])

        child2 = self.manager.save(None, {"name": "Notes", 'slug': 'notes', 'parent': child['uuid'], 'type':  "core.post"})

        self.assertEquals("/new-articles/python-element/notes", child2['path'])

        parent['slug'] = "articles"

        self.manager.save(parent['uuid'], parent)

        child = self.manager.retrieve(child['uuid'])
        child2 = self.manager.retrieve(child2['uuid'])

        self.assertEquals("/articles/python-element", child['path'])
        self.assertEquals("/articles/python-element/notes", child2['path'])

    def test_unique_node(self):
        node1 = self.manager.save(None, {"name": "articles", 'slug': 'articles', 'type':  "core.node"})

        self.assertEquals('/articles', node1['path'])

        with self.assertRaises(DuplicateKeyError):
            node2 = self.manager.save(None, {"name": "articles", 'slug': 'articles', 'type':  "core.node"})


    def test_find_with_invalid_path(self):
        pass

    def tearDown(self):
        self.manager.get_collection().remove()