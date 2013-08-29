import unittest, re

from element.plugins.security.handler import AnonymousAuthenticationHandler, AccessMapListener
from element.plugins.security.security import AnonymousToken, Token
from element.plugins.security.exceptions  import AccessDeniedException, \
    AuthenticationCredentialsNotFoundException, NoRequestFoundException
from element.plugins.security.firewall import AccessMap

from ioc.event import Event

class Request:
    pass

class AnonymousAuthenticationHandlerTest(unittest.TestCase):
    def test_token_not_defined(self):
        e = Event()
        h = AnonymousAuthenticationHandler('provider_name')

        h.handle(e)

        self.assertTrue(e.has('token'))
        self.assertIsInstance(e.get('token'), AnonymousToken)

    def test_token_already_set(self):
        e = Event({
            'token': Token('key', 'user')
        })
        h = AnonymousAuthenticationHandler('provider_name')

        h.handle(e)

        self.assertTrue(e.has('token'))
        self.assertNotIsInstance(e.get('token'), AnonymousToken)

class AccessMapListenerTest(unittest.TestCase):
    def test_no_token(self):
        with self.assertRaises(AuthenticationCredentialsNotFoundException):
           AccessMapListener(AccessMap()).handle(Event())

    def test_no_request(self):

        with self.assertRaises(NoRequestFoundException):
            AccessMapListener(AccessMap()).handle(Event({
                'token': Token('key', 'user')
            }))

    def test_no_rule_in_access_map(self):
        r = Request()
        r.path = ""
        with self.assertRaises(AccessDeniedException):
           AccessMapListener(AccessMap()).handle(Event({
                'token': Token('key', 'user'),
                'request': r
            }))

    def test_match(self):
        r = Request()
        r.path = "/blog/2012/12/12-myblog.html"

        AccessMapListener(AccessMap([(re.compile("/blog.*"), ['IS_AUTHENTICATED_ANONYMOUSLY'])])).handle(Event({
            'token': AnonymousToken('key', 'anon.', 'IS_AUTHENTICATED_ANONYMOUSLY'),
            'request': r
        }))

        # mark the test as valid ...
        self.assertTrue(True)