from flask.views import MethodView, View
import flask

class PathView(MethodView):
    def __init__(self, node_manager, context_creator):
        self.node_manager = node_manager
        self.context_creator = context_creator

    def get(self, path):
        # load the node
        node = self.node_manager.get_node(path)

        if not node:
            flask.abort(404)

        # load the related node's handler
        handler = self.node_manager.get_handler(node)

        if not handler:
            flask.abort(500)
        
        # build the execution context
        context = self.context_creator.build(node, handler)

        # render the response
        return handler.execute(context, flask)
