import unittest
import element.manager

class PackageTest(unittest.TestCase):

    def test_is_uuid(self):

        self.assertTrue(element.manager.is_uuid("fca0ea55-c21b-186e-fe6924a5"))
        self.assertFalse(element.manager.is_uuid("FCA0EA55-C21B-186E-FE6924A5"))
        self.assertFalse(element.manager.is_uuid("salut-comment-ca-ca-bien?"))
