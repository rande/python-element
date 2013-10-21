import yaml, os, functools
import exceptions

class NodeHandler(object):
    pass

class NodeManager(object):
    def __init__(self, db, event_dispatcher, logger=None):
        self.handlers = {}
        self.db = db
        self.event_dispatcher = event_dispatcher
        self.logger = logger

    def add_handler(self, name, handler):
        self.handlers[name] = handler
        handler.code = name

    def get_nodes(self, selector=None, **kwargs):
        nodes = []

        for data in self.db.find(**kwargs):
            nodes.append(Node(data['id'], data['type'] if 'type' in data else None, data))

        event = self.event_dispatcher.dispatch('element.nodes.load.success', {
            'nodes': nodes
        })

        return event.get('nodes')

    def get_node(self, id):
        if self.logger:
            self.logger.debug('NodeManager.get_node: %s' % id)

        if isinstance(id, Node):
            return id

        # clean up this ... not perfect at all...
        try:
            data = self.db.retrieve(id)
        except:
            data = None

        if self.logger:
            self.logger.debug('NodeManager.get_node: %s ~ cannot find node, looking for path' % id)

        if not data:
            data = self.db.find_one(path="/%s" % id)

        # always assume a fail
        event_name = 'element.node.load.fail'
        params = {'id': id}

        if data:
            if self.logger:
                self.logger.debug('NodeManager.get_node: %s ~ Found! ~ %s' % (id, data))

            event_name = 'element.node.load.success'
            params = {
                'node': Node(id, data['type'] if 'type' in data else None, data)
            }

        else:
            if self.logger:
                self.logger.debug('NodeManager.get_node: %s ~ Not Found!' % id)

        event = self.event_dispatcher.dispatch(event_name, params)

        if event.has('node'):
            return event.get('node')

        return None

    def delete(self, node):
        self.event_dispatcher.dispatch('element.node.pre_delete', {
            'node': node,
        })

        result = self.db.delete(node.id)

        self.event_dispatcher.dispatch('element.node.post_delete', {
            'node': node,
        })

        return result
        
    def save(self, node):
        event = self.event_dispatcher.dispatch('element.node.pre_save', {
            'node': node,
            'data': node.data
        })

        result = self.db.save(node.id, node.type, event.get('data'))

        self.event_dispatcher.dispatch('element.node.post_save', {
            'node': node,
            'data': node.data
        })

        return result

    def get_handler(self, node):
        return self.handlers[node.type]

class Node(object):
    def __init__(self, id, type, data=None, manager=None):
        self.id = id
        self.type = type
        self.data = data or {}
        self.methods = {}
        self.manager = manager

    def __getattr__(self, name):
        if name in self.methods:
            return functools.partial(self.methods[name], self)

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