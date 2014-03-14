import element.node
from element.exceptions import PerformanceException

class IndexHandler(element.node.NodeHandler):
    def __init__(self, node_manager, templating):
        self.node_manager = node_manager
        self.templating = templating

    def get_name(self):
        return 'Node Index'

    def get_defaults(self, node):
        if 'filters' not in node.data:
            node.data['filters'] = {}

        if 'types' not in node.data['filters']:
            node.data['filters']['types'] = []

        if 'tags' not in node.data['filters']:
            node.data['filters']['tags'] = []

        if 'category' not in node.data['filters']:
            node.data['filters']['category'] = None

        if 'path' not in node.data['filters']:
            node.data['filters']['path'] = None

        if 'limit' not in node.data['filters']:
            node.data['filters']['limit'] = 64

        if 'offset' not in node.data['filters']:
            node.data['filters']['offset'] = 0

        node.data['filters']['limit'] = int(node.data['filters']['limit'])
        node.data['filters']['offset'] = int(node.data['filters']['offset'])

        return {
            'template': self.get_base_template(node),
        }

    def get_base_template(self, node):
        return node.template or 'element.plugins.node:index.html'

    def execute(self, request_handler, context):
        if context.filters['limit'] > 128:
            raise PerformanceException("The limit cannot be greater than 128 (limit:%s)" % context.filters['limit'])

        nodes = self.node_manager.get_nodes(**{
            'types':    context.filters['types'], 
            'limit':    context.filters['limit'], 
            'offset':   context.filters['offset'], 
            'category': context.filters['category'], 
            'tags':     context.filters['tags'], 
            'path':     context.filters['path'],
        })

        nodes.sort(key=lambda node: node.data['published_at'], reverse=True)

        self.render(request_handler, self.templating, context.settings['template'], {
            'context': context,
            'nodes': nodes
        })
