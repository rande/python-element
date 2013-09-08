from node import NodeContext

class ContextCreator(object):
    def __init__(self, defaults=None):
        self.defaults = defaults or {
            'base_template': 'element:base.html',
        }
        
    def build(self, node, handler, defaults=None):
        settings = {}

        settings.update(self.defaults)
        settings.update(node.data)
        settings.update(handler.get_defaults(node))
        settings.update(defaults or {})

        if not settings['base_template']:
            settings['base_template'] = 'element:empty.html'

        return NodeContext(node, settings)