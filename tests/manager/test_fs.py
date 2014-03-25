# vim: set fileencoding=utf-8 :
import unittest
import element.manager.fs
import element.loaders
import element.plugins.static.loader
import os
import shutil
import element.exceptions

class FsManagerTest(unittest.TestCase):     
    def setUp(self):
        self.fixture = "%s/../fixtures/data/" % os.path.dirname(os.path.abspath(__file__))
        self.fs = element.manager.fs.FsManager(
            self.fixture, 
            element.loaders.LoaderChain([
                ('yaml', element.loaders.YamlNodeLoader()),
                ('static', element.plugins.static.loader.StaticNodeLoader({
                    'jpg': 'image/jpeg',
                    'png': 'image/png',
                })),
            ])
        )

        if os.path.isdir('%s/tmp' % self.fixture):
            shutil.rmtree('%s/tmp' % self.fixture)

        self.fs.build_references()

    def tearDown(self):
        if os.path.isdir('%s/tmp' % self.fixture):
            shutil.rmtree('%s/tmp' % self.fixture)


    def test_build_references(self):
        self.fs.build_references()

        self.assertEquals(2, len(self.fs.files))

        expected = {
            'fca0ea55-c21b-186e-fe6924a5': 'sonata_small.png',
            'c3e6be59-3448-0daa-be2dd043': '2013/my-post-content'
        }

        self.assertEquals(expected, self.fs.files)

    def test_contains_uuid(self):
        node = self.fs.retrieve("sonata_small.png")

        self.assertEquals(node['id'], "sonata_small.png")
        self.assertEquals(node['uuid'], "fca0ea55-c21b-186e-fe6924a5")

    def test_retrieve(self):
        node = self.fs.retrieve('fca0ea55-c21b-186e-fe6924a5')

        self.assertEquals(node['id'], "sonata_small.png")
        self.assertEquals(node['uuid'], "fca0ea55-c21b-186e-fe6924a5")

        node = self.fs.retrieve("sonata_small.png")

        self.assertEquals(node['id'], "sonata_small.png")
        self.assertEquals(node['uuid'], "fca0ea55-c21b-186e-fe6924a5")

    def test_exists(self):
        self.assertTrue(self.fs.exists('fca0ea55-c21b-186e-fe6924a5'))
        self.assertTrue(self.fs.exists('sonata_small.png'))

    def test_find(self):
        cases = [
            ({}, 2),
            ({'type': 'blog.post'}, 1),
            ({'type': 'fake'}, 0),
            ({'type': 'fake', 'types': ['blog.post']}, 1),
            ({'types': ['blog.post', 'fake']}, 1),
            ({'types': [], 'tags': ['red', 'yellow']}, 1),
            ({'types': [], 'tags': ['red', 'yellow', 'brown']}, 0),
            ({'types': [], 'tags': []}, 2)
        ]

        for kwarg, expected in cases:
            nodes = self.fs.find(**kwarg)
            self.assertEquals(expected, len(nodes))

    def test_private(self):
        cases = [
            ({'path': "/../private"}, 0),
        ]

        for kwarg, expected in cases:
            with self.assertRaises(element.exceptions.SecurityAccessException):
                self.fs.find(**kwarg)

    def test_save_and_delete(self):
        self.assertFalse(self.fs.delete('tmp/simple_save'))
        self.assertTrue(self.fs.save('tmp/simple_save', {'hello': 'world', 'type': 'mytype'}))
        self.assertTrue(self.fs.delete('tmp/simple_save'))

    def test_save_nested_folder(self):
        self.assertTrue(self.fs.save('tmp/nested/fake', {'hello': 'world', 'type': 'mytype'}))
        
    def test_save_binary_file(self):
        self.assertTrue(self.fs.save('tmp/foo/image.png', {
            'type': 'element.static',
            'content': file("%s/sonata_small.png" % self.fixture, 'r').read()
        }))

        self.assertTrue(os.path.isfile("%s/tmp/foo/image.png" % self.fixture))
