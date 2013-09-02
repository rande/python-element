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