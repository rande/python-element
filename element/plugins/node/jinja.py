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

        return self.unicode(request_handler.get_buffer())

    def render_node_event(self, event_name, options=None):
        event = self.dispatcher.dispatch(event_name, options or {})

        if not event.has('node'):
            return "<!-- no listener registered for event: %s -->" % event_name

        return self.unicode(self.render_node(event.get('node')))

    def unicode(self, content):
        if isinstance(content, unicode):
            return content

        return content.decode("utf-8")

class ResponseListener(object):
    def __init__(self, templating):
        self.templating = templating

    def handle(self, event):

        result = event.get('result')

        if not isinstance(result, tuple):
            return

        request_handler = event.get('request_handler')
        status_code, template_name, params = result

        request_handler.set_status(status_code)
        request_handler.write(self.templating.get_template(template_name).render(params))
