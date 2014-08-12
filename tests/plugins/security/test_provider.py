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