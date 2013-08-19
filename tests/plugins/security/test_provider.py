
# vim: set fileencoding=utf-8 :
import unittest
from element.plugins.security.provider import InMemoryProvider
from element.plugins.security.exceptions import UsernameNotFoundException
from element.plugins.security.user import User

class InMemoryProviderTest(unittest.TestCase):

    def setUp(self):
        self.provider = InMemoryProvider([
            {'username': 'foo', 'password': 'bar', 'roles': []},
            {'username': 'bar'}
        ])

    def test_init_valid_users(self):
        self.assertEquals(2, len(self.provider.users))
        self.assertEquals('foo', self.provider.users['foo'].username)
        self.assertEquals('bar', self.provider.users['foo'].password)

        self.assertEquals('bar', self.provider.users['bar'].username)
        self.assertEquals(None, self.provider.users['bar'].password)

    def test_find_by_username(self):

        with self.assertRaises(UsernameNotFoundException):
            self.provider.loadUserByUsername('fake')

        user = self.provider.loadUserByUsername('bar')

        self.assertEquals('bar', user.username)

    def test_refresh_user(self):

        user = self.provider.loadUserByUsername('bar')

        user = self.provider.refreshUser(user)

        self.assertEquals('bar', user.username)

    def test_support_class(self):
        self.assertTrue(self.provider.supportClass(User))