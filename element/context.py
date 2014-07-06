from node import NodeContext

class ContextCreator(object):
    def __init__(self, event_dispatcher, defaults=None):
        self.event_dispatcher = event_dispatcher
        self.defaults = defaults or {
            'base_template': 'element:base.html',
        }
        
    def build(self, node, handler, defaults=None):
        settings = {}

        settings.update(self.defaults)
        settings.update(handler.get_defaults(node))
        settings.update(node.data)
        settings.update(defaults or {})

        if not settings['base_template']:
            settings['base_template'] = 'element:empty.html'

        context = NodeContext(node, settings)

        self.event_dispatcher.dispatch('element.node.context.load', {
            'context': context
        })

        return context