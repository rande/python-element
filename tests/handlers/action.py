
# vim: set fileencoding=utf-8 :
import unittest
import ioc.component
import element.node, element.handlers.action
import flask
import werkzeug.wrappers

class RedictHandlerTest(unittest.TestCase):
    def setUp(self):
        self.handler = element.handlers.action.RedirectHandler("/baseurl")


    def test_get_defaults(self):
        self.assertEquals({}, self.handler.get_defaults({}))

    def test_execute_relative(self):

        context = element.node.NodeContext(
            element.node.Node('myid', 'mytype', {'redirect': 'to'})
        )

        response = self.handler.execute(context, flask)

        self.assertIsInstance(response, werkzeug.wrappers.BaseResponse)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.headers.get('Location'), '/baseurl/myid/to')


    def test_execute_absolute(self):

        context = element.node.NodeContext(
            element.node.Node('myid', 'mytype', {'redirect': '/to'})
        )

        response = self.handler.execute(context, flask)

        self.assertIsInstance(response, werkzeug.wrappers.BaseResponse)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.headers.get('Location'), '/baseurl/to')

    def test_execute_absolute_scheme(self):

        context = element.node.NodeContext(
            element.node.Node('myid', 'mytype', {'redirect': 'http://github.com'})
        )

        response = self.handler.execute(context, flask)

        self.assertIsInstance(response, werkzeug.wrappers.BaseResponse)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.headers.get('Location'), 'http://github.com')