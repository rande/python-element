import element.node
import markdown
from tornado.web import RequestHandler
from tornado.httpserver import HTTPRequest

class SubRequestHandler(RequestHandler):
    def get_buffer(self):
        return b"".join(self._write_buffer)

class Core(object):
    def __init__(self, node_manager, context_creator, dispatcher, application):
        self.node_manager = node_manager
        self.context_creator = context_creator
        self.dispatcher = dispatcher
        self.application = application

    def render_node(self, node, defaults=None):
        defaults = defaults or {}

        # load the node
        node = self.node_manager.get_node(node)

        if not node:
            return "<!-- unable to found the node -->"

        # load the related node's handler
        handler = self.node_manager.get_handler(node)

        if not handler:
            return "<!-- unable to found the node handler -->"
        
        # build the execution context
        context = self.context_creator.build(node, handler, defaults)

        # create a sub request handler to retrieve the buffer and return it as string
        request_handler = SubRequestHandler(self.application, HTTPRequest('GET', '/_internal'))

        # render the response
        handler.execute(request_handler, context)

        return request_handler.get_buffer()

    def render_node_event(self, event_name, options=None):
        event = self.dispatcher.dispatch(event_name, options or {})

        if not event.has('node'):
            return "<!-- no listener registered for event: %s -->" % event_name

        return self.render_node(event.get('node'))

    def markup(self, content, format=None):
        if isinstance(content, element.node.NodeContext):
            format = content.node.format
            content = content.node.content

        if isinstance(content, element.node.Node):
            format = content.format
            content = content.content

        if format == 'markdown':
            return markdown.markdown(content)

        return content