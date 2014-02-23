# vim: set fileencoding=utf-8 :
import unittest
import element.context
import element.node
import mock

class ContextCreatorTest(unittest.TestCase):
    def test_build(self):
        creator = element.context.ContextCreator()

        handler = mock.Mock()
        handler.get_defaults.return_value = {}

        node = element.node.Node(None, "test")

        context = creator.build(node, handler)

        self.assertIsInstance(context, element.node.NodeContext)
        self.assertEquals(context.node.type, "test")
        self.assertEquals(context.base_template, "element:base.html")
