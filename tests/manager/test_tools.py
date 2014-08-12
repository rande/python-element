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

from element.manager.tools import ChainManager
import mock

class ChainManagerTest(unittest.TestCase):
    def test_with_no_manager(self):
        manager = ChainManager(None)

        with self.assertRaises(Exception):
            manager.retrieve("none")

        self.assertFalse(manager.exists("id"))
        self.assertFalse(manager.delete("id"))

    def test_with_no_manager_invalid_data(self):

        manager = ChainManager(None)

        with self.assertRaises(Exception):
            manager.save("reference", "blog.text", {})

    def test_with_no_manager_valid_data(self):

        manager = ChainManager(None)

        self.assertFalse(manager.save("reference", {'manager': 'foobar', "type": "blog.text"}))

    def test_with_no_manager_and_find(self):
        manager = ChainManager(None)

        self.assertEquals([], manager.find())
        self.assertEquals(None, manager.find_one())


    def test_with_managers_retrieve(self):
        m = mock.Mock()
        m.retrieve.return_value = {"salut": "les gens!"}

        manager = ChainManager([("fs", m)])
        n = manager.retrieve("hello")

        self.assertEquals("fs", n["manager"])

    def test_with_managers_exists(self):
        m = mock.Mock()
        m.exists.return_value = True

        manager = ChainManager([("fs", m)])
        self.assertTrue(manager.exists("hello"))

    def test_with_managers_delete(self):
        m = mock.Mock()
        m.delete.return_value = True

        manager = ChainManager([("fs", m)])

        self.assertTrue(manager.delete("hello"))

    def test_with_managers_save(self):
        m = mock.Mock()
        m.save.return_value = True

        manager = ChainManager([("fs", m)])

        self.assertTrue(manager.save("id", {"manager": "fs", "hello": "les gens!", "type": "blog.post"}))
        self.assertFalse(manager.save("id", {"manager": "mongo", "hello": "les gens!", "type": "blog.post"}))

    def test_with_managers_find(self):
        m = mock.Mock()
        m.find.return_value = [{"name": "thomas"}, {"name": "nicolas"}]

        manager = ChainManager([("fs", m)])
        results = manager.find()

        self.assertEquals(2, len(results))
        self.assertEquals("thomas", results[0]['name'])
        self.assertEquals("nicolas", results[1]['name'])

        results = manager.find(limit=1)

        self.assertEquals(1, len(results))

        self.assertEquals("fs", results[0]['manager'])
        self.assertEquals("thomas", results[0]['name'])

        results = manager.find(limit=1, offset=1)

        self.assertEquals(1, len(results))
        self.assertEquals("fs", results[0]['manager'])
        self.assertEquals("nicolas", results[0]['name'])

    def test_with_managers_find_one(self):
        m = mock.Mock()
        m.find.return_value = [{"name": "thomas"}, {"name": "nicolas"}]

        manager = ChainManager([("fs", m)])
        result = manager.find_one()

        self.assertEquals("fs", result['manager'])
        self.assertEquals("thomas", result['name'])


    def test_with_manager_name(self):
        m_fs = mock.Mock()
        m_fs.find.return_value = [{"name": "thomas FS"}, {"name": "nicolas FS"}]

        m_mongo = mock.Mock()
        m_mongo.find.return_value = [{"name": "thomas Mongo"}, {"name": "nicolas Mongo"}]

        manager = ChainManager([("fs", m_fs), ("mongo", m_mongo)])
        result = manager.find_one(manager="fs")

        self.assertEquals("fs", result['manager'])
        self.assertEquals("thomas FS", result['name'])

        result = manager.find_one(manager="mongo")

        self.assertEquals("mongo", result['manager'])
        self.assertEquals("thomas Mongo", result['name'])