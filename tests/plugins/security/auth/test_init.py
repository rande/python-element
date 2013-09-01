import unittest

from element.plugins.security.auth import DaoAuthenticationProvider, AuthenticationProviderManager
from element.plugins.security.provider import InMemoryProvider
from element.plugins.security.security import Token
from element.plugins.security.exceptions import UsernameNotFoundException, BadCredentialsException
from ioc.event import Dispatcher

class DaoAuthenticationProviderTest(unittest.TestCase):

    def test_support(self):
        auth_provider = DaoAuthenticationProvider(InMemoryProvider(), 'admin')

        self.assertFalse(auth_provider.supports(Token('foo', 'anno.')))
        self.assertTrue(auth_provider.supports(Token('admin', 'anno.')))

    def test_authenticate_exception(self):
        provider = InMemoryProvider([
            {'username': 'foo', 'password': 'bar', 'roles': ['ADMIN']},
            {'username': 'bar'}
        ])

        auth_provider = DaoAuthenticationProvider(provider, 'admin')

        with self.assertRaises(UsernameNotFoundException):
            auth_provider.authenticate(Token('admin', 'anno.'))

        with self.assertRaises(BadCredentialsException):
            t = Token('admin', 'foo')
            t.credentials = 'fake password'
            auth_provider.authenticate(t)

    def test_authenticate(self):
        provider = InMemoryProvider([
            {'username': 'foo', 'password': 'bar', 'roles': ['ADMIN']},
            {'username': 'bar'}
        ])

        auth_provider = DaoAuthenticationProvider(provider, 'admin')

        t = Token('admin', 'foo')
        t.credentials = 'bar'
        token = auth_provider.authenticate(t)

        self.assertEquals(['ADMIN'], token.roles)

class AuthenticationProviderManagerTest(unittest.TestCase):
    def test_authenticate(self):

        auth_provider = DaoAuthenticationProvider(InMemoryProvider(), 'admin')

        auth_manager = AuthenticationProviderManager(Dispatcher(), [auth_provider])

        t = Token('admin', 'foo')
        t.credentials = 'bar'

        with self.assertRaises(UsernameNotFoundException):
            auth_manager.authenticate(t)

        

