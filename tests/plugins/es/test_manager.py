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

__author__ = 'rande'

import unittest
from element.plugins.es.manager import ElasticSearchManager, Elasticsearch
from element.manager import get_uuid, generate_uuid, InvalidDataFormat, InvalidTreeState
import time

class ElasticSearchManagerTest(unittest.TestCase):
    def setUp(self):
        self.client = Elasticsearch()

        self.client.indices.delete(index='test_element', ignore=404)

        self.manager = ElasticSearchManager(index='test_element')

        self.client.index(doc_type='node', refresh=True, index='test_element', body={
            "uuid": "b875b4ea-9682-aeaf-2dec4c5e",
            "author": "Mike",
            "text": "My first blog post!",
            "slug": "my-first-blog-post",
            "parent": None,
            "path": "/myfirst-blog-post",
            "tags": ["mongodb", "python", "pymongo"],
            "type": 'node.text'
        })

        self.client.index(doc_type='node', refresh=True, index='test_element', body={
            "uuid": "b875b4ea-9682-aeaf-2dec4c5f",
            "author": "Mike",
            "text": "My First Page",
            "slug": "my-page",
            "parent": None,
            "path": "/mypage",
            "tags": ["mongodb"],
            "type": 'node.page'
        })

    def test_retrieve(self):
        self.assertIsNone(self.manager.retrieve("ad"))
        self.assertIsNone(self.manager.retrieve("casdsb4ea-9682-aeaf-2dec4c5e"))

        self.assertTrue(self.manager.exists("b875b4ea-9682-aeaf-2dec4c5e"))
        data = self.manager.retrieve("b875b4ea-9682-aeaf-2dec4c5e")
        self.assertIsNotNone(data)

    def test_exists(self):
        self.assertFalse(self.manager.exists("c875b4ea-9682-aeaf-2dec4c5e"))
        self.assertTrue(self.manager.exists("b875b4ea-9682-aeaf-2dec4c5e"))

    def test_delete(self):
        self.assertTrue(self.manager.delete("b875b4ea-9682-aeaf-2dec4c5e"))
        self.assertTrue(self.manager.delete("b875b4ea-9682-aeaf-2dec4c5e"))
        self.assertFalse(self.manager.exists("b875b4ea-9682-aeaf-2dec4c5e"))

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

        self.assertTrue(self.manager.exists(parent['uuid']))

        self.assertEquals('/articles', parent['path'])
        child = self.manager.save(None, {"type": "core.post", "name": "Python Element", 'slug': 'python-element', 'parent': parent['uuid']})

        self.assertEquals('/articles/python-element', child['path'])

    def test_save_with_children(self):
        parent = self.manager.save(None, {"name": "articles", 'slug': 'articles', 'type': "core.node"})
        child = self.manager.save(None, {"name": "Python Element", 'slug': 'python-element', 'parent': parent['uuid'], 'type':  "core.post"})

        self.assertEquals('/articles/python-element', child['path'])

        parent['slug'] = 'new-articles'

        parent = self.manager.save(parent['uuid'], parent)

        self.assertEquals("/new-articles", parent['path'])

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

    def test_find_by_type(self):
        results = self.manager.find(type='node.text')

        self.assertEquals(len(results), 1)

    def test_find_with_invalid_path(self):
        pass

    def tearDown(self):
        self.client.delete_by_query(index='test_element', body='{"query":{"match_all":{}}}')