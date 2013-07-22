
# vim: set fileencoding=utf-8 :
import unittest
import ioc.component
import element.node, element.plugins.action
import flask
import ioc.exceptions
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

class ActionHandlerTest(unittest.TestCase):
    def setUp(self):
        self.container = ioc.component.Container()
        self.handler = element.handlers.action.ActionHandler(self.container)

        app = flask.Flask('AAA')
        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_non_existant_service(self):
        context = element.node.NodeContext(
            element.node.Node("id", "mytype")
        )

        self.assertRaises(ioc.exceptions.UnknownService, self.handler.execute, context, flask)


    def test_return_response(self):
        context = element.node.NodeContext(
            element.node.Node("id", "mytype", {'serviceId': 'fake', 'method': 'foo'})
        )

        class Fake(object):
            def foo(self, context, **kwargs):
                return context.flask.make_response("a response")

        self.container.add('fake', Fake())
        response = self.handler.execute(context, flask)

        self.assertIsInstance(response, werkzeug.wrappers.BaseResponse)
        self.assertEquals(response.status_code, 200)