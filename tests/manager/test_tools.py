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

        self.assertFalse(manager.save("reference", "blog.text", {'manager': 'foobar'}))

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

        self.assertTrue(manager.save("id", "blog.post", {"manager": "fs", "hello": "les gens!"}))
        self.assertFalse(manager.save("id", "blog.post", {"manager": "mongo", "hello": "les gens!"}))

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

