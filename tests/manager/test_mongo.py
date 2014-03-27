import unittest
import ioc.event
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from element.manager.mongo import MongoManager, InvalidDataFormat
from pymongo.errors import DuplicateKeyError

class MongoManagerTest(unittest.TestCase):
    def setUp(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.manager = MongoManager(self.client, '_ci_python_element_test', '_ci_python_collection')
        self.manager.get_collection().remove()

        self.manager.get_collection().insert({
            "_id": ObjectId("507f1f77bcf86cd799439012"),
            "author": "Mike",
            "text": "My first blog post!",
            "slug": "my-first-blog-post",
            "parent": None,
            "path": "/myfirst-blog-post",
            "tags": ["mongodb", "python", "pymongo"],
        })

    def test_retrieve(self):
        self.assertIsNone(self.manager.retrieve("ad"))
        self.assertIsNone(self.manager.retrieve("507f1f77bcf86cd799439011"))
        data = self.manager.retrieve("507f1f77bcf86cd799439012")
        self.assertIsNotNone(data)
        self.assertTrue("id" in data)

    def test_exists(self):
        self.assertFalse(self.manager.exists("507f1f77bcf86cd799439011"))
        self.assertTrue(self.manager.exists("507f1f77bcf86cd799439012"))

    def test_delete(self):
        self.assertEquals(1, self.manager.delete("507f1f77bcf86cd799439012"))
        self.assertEquals(0, self.manager.delete("507f1f77bcf86cd799439011"))

    def test_save_no_parent(self):
        with self.assertRaises(InvalidDataFormat):
            self.manager.save("507f1f77bcf86cd799439010", {"type":"core.user", "name": "Thomas Rabaix"})

        data = self.manager.save("507f1f77bcf86cd799439010", {"type": "core.user", "name": "Thomas Rabaix", "slug": "thomas-rabaix"})

        self.assertTrue("id" in data)
        self.assertEquals("507f1f77bcf86cd799439010", data['id'])

        self.assertIsNotNone(data['id'])
        self.assertIsNone(data['parent'])
        self.assertEquals("/thomas-rabaix", data['path'])

    def test_save_with_parent_no_child(self):
        parent = self.manager.save(None, {"type": "core.node", "name": "articles", 'slug': 'articles'})

        self.assertEquals('/articles', parent['path'])

        child = self.manager.save(None, {"type": "core.post", "name": "Python Element", 'slug': 'python-element', 'parent': parent['id']})

        self.assertEquals('/articles/python-element', child['path'])

    def test_save_with_children(self):
        parent = self.manager.save(None, {"name": "articles", 'slug': 'articles', 'type': "core.node"})
        child = self.manager.save(None, {"name": "Python Element", 'slug': 'python-element', 'parent': parent['id'], 'type':  "core.post"})

        parent['slug'] = 'new-articles'
        self.manager.save(parent['id'], parent)
        child = self.manager.retrieve(child['id'])

        self.assertEquals("/new-articles/python-element", child['path'])

        child2 = self.manager.save(None, {"name": "Notes", 'slug': 'notes', 'parent': child['id'], 'type':  "core.post"})

        self.assertEquals("/new-articles/python-element/notes", child2['path'])

        parent['slug'] = "articles"

        self.manager.save(parent['id'], parent)

        child = self.manager.retrieve(child['id'])
        child2 = self.manager.retrieve(child2['id'])

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