import flask
import element.node
import markdown

class Core(object):
    def __init__(self, node_manager, context_creator, dispatcher):
        self.node_manager = node_manager
        self.context_creator = context_creator
        self.dispatcher = dispatcher

    def render_node(self, node, defaults=None):
        defaults = defaults or {}

        # load the node
        node = self.node_manager.get_node(node)

        if not node:
            return "<!-- unable to found the node -->";

        # load the related node's handler
        handler = self.node_manager.get_handler(node)

        if not handler:
            return "<!-- unable to found the node handler -->";
        
        # build the execution context
        context = self.context_creator.build(node, handler, defaults)

        # render the response
        return handler.execute(context, flask).data

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