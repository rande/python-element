import unittest, re

from element.plugins.security.handler import AnonymousAuthenticationHandler, AccessMapListener
from element.plugins.security.security import AnonymousToken, Token, SecurityContext
from element.plugins.security.exceptions  import AccessDeniedException, \
    AuthenticationCredentialsNotFoundException, NoRequestFoundException
from element.plugins.security.firewall import AccessMap
from element.plugins.security.role import RoleHierarchy

from ioc.event import Event

class Request:
    pass

class AnonymousAuthenticationHandlerTest(unittest.TestCase):
    def test_token_not_defined(self):
        e = Event()
        c = SecurityContext()
        h = AnonymousAuthenticationHandler('provider_name', c)

        h.handle(e)

        self.assertIsInstance(c.token, AnonymousToken)

    def test_token_already_set(self):
        c = SecurityContext()
        c.token = Token('key', 'user')

        e = Event()
        h = AnonymousAuthenticationHandler('provider_name', c)

        h.handle(e)

        self.assertNotIsInstance(c.token, AnonymousToken)

class AccessMapListenerTest(unittest.TestCase):
    def test_no_token(self):
        with self.assertRaises(AuthenticationCredentialsNotFoundException):
           AccessMapListener(AccessMap()).handle(Event(), SecurityContext(), RoleHierarchy())

    def test_no_request(self):

        context = SecurityContext()
        context.token = Token('key', 'user')

        with self.assertRaises(NoRequestFoundException):
            AccessMapListener(AccessMap(), context, RoleHierarchy()).handle(Event())

    def test_no_rule_in_access_map(self):
        r = Request()
        r.path = ""

        context = SecurityContext()
        context.token = Token('key', 'user')

        with self.assertRaises(AccessDeniedException):
           AccessMapListener(AccessMap(), context, RoleHierarchy()).handle(Event({
                'request': r
            }))

    def test_no_token(self):
        r = Request()
        r.path = "/blog/2012/12/12-myblog.html"

        context = SecurityContext()
        context.token = AnonymousToken('key', 'anon.', 'IS_AUTHENTICATED_ANONYMOUSLY')
        
        AccessMapListener(AccessMap([(re.compile("/blog.*"), ['IS_AUTHENTICATED_ANONYMOUSLY'])]), context, RoleHierarchy()).handle(Event({
            'request': r
        }))

        # mark the test as valid ...
        self.assertTrue(True)

    def test_match(self):
        r = Request()
        r.path = "/blog/2012/12/12-myblog.html"

        context = SecurityContext()
        context.token = AnonymousToken('key', 'anon.', 'IS_AUTHENTICATED_ANONYMOUSLY')

        AccessMapListener(AccessMap([(re.compile("/blog.*"), ['IS_AUTHENTICATED_ANONYMOUSLY'])]), context, RoleHierarchy()).handle(Event({
            'request': r
        }))

        # mark the test as valid ...
        self.assertTrue(True)