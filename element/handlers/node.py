import markdown, os
import element.handlers
import datetime

class IndexHandler(element.handlers.NodeHandler):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def get_defaults(self, node):
        if 'filters' not in node.data:
            node.data['filters'] = {
                'types': [],
                'category': None,
                'tags': [],
                'path': None
            }

        if 'types' not in node.data['filters']:
            node.data['filters']['types'] = []

        if 'tags' not in node.data['filters']:
            node.data['filters']['tags'] = []

        if 'category' not in node.data['filters']:
            node.data['filters']['category'] = None

        if 'path' not in node.data['filters']:
            node.data['filters']['path'] = None

        defaults = {
            'template': self.get_base_template(),
            'path': node.data['filters']['path'],
            'types': node.data['filters']['types'],
            'tags': node.data['filters']['tags'],
            'category': node.data['filters']['category'],
            'link': node.link,
        }

        return defaults

    def get_base_template(self):
        return 'element:handlers/node/index.html'

    def execute(self, context, flask):
        now = datetime.datetime.now()

        nodes = self.node_manager.get_nodes(
            path=context.path,
            type=context.type,
            types=context.types, 
            category=context.category,
            tags=context.tags,
            selector=lambda node: now > node.published_at
        )

        nodes.sort(key=lambda node: node.data['published_at'], reverse=True)

        params = {
            'context': context,
            'nodes': nodes
        }

        return flask.make_response(flask.render_template(context.settings['template'], **params))