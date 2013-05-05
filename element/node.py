import yaml, os

class NodeManager(object):
    def __init__(self, event_dispatcher):
        self.handlers = {}
        self.loaders = {}
        self.event_dispatcher = event_dispatcher

    def add_handler(self, name, handler):
        self.handlers[name] = handler

    def add_loader(self, name, loader):
        self.loaders[name] = loader

    def get_node(self, id):
        node = None

        if isinstance(id, Node):
            return id
            
        for name, loader in self.loaders.iteritems():
            if loader.supports(id):
                node = loader.load(id)

                break

        if not node:
            event = self.event_dispatcher.dispatch('element.node.load.fail', {
                'id': id
            })
        else:
            event = self.event_dispatcher.dispatch('element.node.load.success', {
                'node': node
            })
        
        if event.has('node'):
            return event.get('node')

        return None

    def get_handler(self, node):
        return self.handlers[node.type]

class Node(object):
    def __init__(self, id, type, data=None):
        self.id = id
        self.type = type
        self.data = data or {}

    def __getattr__(self, name):
        return self.data[name]

class NodeContext(object):
    def __init__(self, node, settings=None):
        self.node = node
        self.settings = settings or {}
