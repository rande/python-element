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

from element.plugins.security.auth import DaoAuthenticationProvider, AuthenticationProviderManager
from element.plugins.security.provider import InMemoryProvider
from element.plugins.security.security import UsernamePasswordToken
from element.plugins.security.exceptions import UsernameNotFoundException, BadCredentialsException
from ioc.event import Dispatcher

class DaoAuthenticationProviderTest(unittest.TestCase):

    def test_support(self):
        auth_provider = DaoAuthenticationProvider(InMemoryProvider(), 'admin')

        self.assertFalse(auth_provider.supports(UsernamePasswordToken('foo', 'anno.')))
        self.assertTrue(auth_provider.supports(UsernamePasswordToken('admin', 'anno.')))

    def test_authenticate_exception(self):
        provider = InMemoryProvider([
            {'username': 'foo', 'password': 'bar', 'roles': ['ADMIN']},
            {'username': 'bar'}
        ])

        auth_provider = DaoAuthenticationProvider(provider, 'admin')

        with self.assertRaises(UsernameNotFoundException):
            auth_provider.authenticate(UsernamePasswordToken('admin', 'anno.'))

        with self.assertRaises(BadCredentialsException):
            t = UsernamePasswordToken('admin', 'foo')
            t.credentials = 'fake password'
            auth_provider.authenticate(t)

    def test_authenticate(self):
        provider = InMemoryProvider([
            {'username': 'foo', 'password': 'bar', 'roles': ['ADMIN']},
            {'username': 'bar'}
        ])

        auth_provider = DaoAuthenticationProvider(provider, 'admin')

        t = UsernamePasswordToken('admin', 'foo')
        t.credentials = 'bar'
        token = auth_provider.authenticate(t)

        self.assertEquals(['ADMIN'], token.roles)

class AuthenticationProviderManagerTest(unittest.TestCase):
    def test_authenticate(self):

        auth_provider = DaoAuthenticationProvider(InMemoryProvider(), 'admin')

        auth_manager = AuthenticationProviderManager(Dispatcher(), [auth_provider])

        t = UsernamePasswordToken('admin', 'foo')
        t.credentials = 'bar'

        with self.assertRaises(UsernameNotFoundException):
            auth_manager.authenticate(t)
