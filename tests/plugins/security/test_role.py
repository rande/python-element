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

from element.plugins.security.role import RoleHierarchy

class RoleHierarchyTest(unittest.TestCase):
    def test_get_roles(self):
        r = RoleHierarchy({
            # ADMIN == SUPER_ADMIN (self referencing)
            'ROLE_ADMIN': ['ROLE_DEFAULT', 'ROLE_SUPER_ADMIN'],
            'ROLE_SUPER_ADMIN': ['ROLE_ADMIN', 'ROLE_FOO'],
            'ROLE_DEFAULT': ['ROLE_USER'],
        })

        expected = {
            'ROLE_SUPER_ADMIN': ['ROLE_ADMIN', 'ROLE_FOO', 'ROLE_USER', 'ROLE_DEFAULT', 'ROLE_SUPER_ADMIN'],
            'ROLE_ADMIN': ['ROLE_SUPER_ADMIN', 'ROLE_ADMIN', 'ROLE_USER', 'ROLE_FOO', 'ROLE_DEFAULT'],
            'ROLE_DEFAULT': ['ROLE_DEFAULT', 'ROLE_USER']
        }

        for name, value in expected.iteritems():
            self.assertItemsEqual(value, r.roles[name])

        self.assertItemsEqual(
            ['ROLE_SUPER_ADMIN', 'ROLE_ADMIN', 'ROLE_USER', 'ROLE_FOO', 'ROLE_DEFAULT'], 
            r.get_reachable_roles(['ROLE_ADMIN'])
        )

        self.assertItemsEqual(
            ['ROLE_SUPER_ADMIN', 'ROLE_ADMIN', 'ROLE_USER', 'ROLE_FOO', 'ROLE_DEFAULT'], 
            r.get_reachable_roles(['ROLE_SUPER_ADMIN', 'ROLE_ADMIN'])
        )