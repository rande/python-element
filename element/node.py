import yaml, os
import element.node

class NodeManager(object):
    def __init__(self, db, event_dispatcher):
        self.handlers = {}
        self.db = db
        self.event_dispatcher = event_dispatcher

    def add_handler(self, name, handler):
        self.handlers[name] = handler

    def get_nodes(self, selector=None, **kwargs):
        nodes = []

        for data in self.db.find(**kwargs):
            nodes.append(element.node.Node(data['id'], data['type'] if 'type' in data else None, data))

        event = self.event_dispatcher.dispatch('element.nodes.load.success', {
            'nodes': nodes
        })

        return event.get('nodes')

    def get_node(self, id):
        node = None

        if isinstance(id, Node):
            return id
        
        data = self.db.retrieve(id)

        # always assume a fail
        event_name = 'element.node.load.fail'
        params = {'id': id}

        if data:
            event_name = 'element.node.load.success'
            params = {'node': element.node.Node(id, data['type'] if 'type' in data else None, data)}

        event = self.event_dispatcher.dispatch(event_name, params)

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
        if name in self.data:
            return self.data[name]

        return None

class NodeContext(object):
    def __init__(self, node, settings=None):
        self.node = node
        self.settings = settings or {}

    def __getattr__(self, name):
        if name in self.settings:
            return self.settings[name]

        return None