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

from element.plugins.security.exceptions import AuthenticationCredentialsNotFoundException
from element.plugins.security.security import SecurityContext, AnonymousToken

class SecurityContextTest(unittest.TestCase):
    def test_is_granted_with_no_token(self):
        context = SecurityContext()

        with self.assertRaises(AuthenticationCredentialsNotFoundException):
            context.is_granted('role')

    def test_is_granted(self):
        context = SecurityContext()

        context.token = AnonymousToken('provider', 'ann.')

        self.assertFalse(context.is_granted(''))
        self.assertFalse(context.is_granted('role'))

        context.token.roles.append('role')

        self.assertTrue(context.is_granted('role'))



