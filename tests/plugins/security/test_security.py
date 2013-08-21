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



