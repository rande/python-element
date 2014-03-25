import yaml, os, functools
import uuid, datetime
from element.exceptions import InvalidDataException

class NodeHandler(object):
    def render(self, request_handler, templating, template_name, params):
        template = templating.get_template(template_name)

        return request_handler.write(template.render(params))

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
            nodes.append(Node(data['id'], data))

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
            self.logger.debug('NodeManager.get_node: %s ~ cannot find node with id, looking for path' % id)

        if not data:
            data = self.db.find_one(path="/%s" % id)

            if data and data['path'] != "/%s" % id:
                data = None

        # always assume a fail
        event_name = 'element.node.load.fail'
        params = {'id': id}

        if data:
            if self.logger:
                self.logger.debug('NodeManager.get_node: %s ~ Found! ~ %s' % (id, data))

            event_name = 'element.node.load.success'
            params = {
                'node': Node(id, data)
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
    def __init__(self, nid, data=None):

        self.methods = {}
        self.id = nid

        self.manager = None
        # set default values

        self.uuid = uuid.uuid4()
        self.data = {}
        self.type = None
        self.enabled = True
        self.status = 0
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.version = 1
        self.revision = 1
        self.deleted = False
        self.current = True
        self.set_uuid = None
        self.weight = 0
        self.set = None

        if not data:
            return

        for name, value in data.iteritems():
            if name == 'id':
                continue

            if name in self.__dict__:
                self.__setattr__(name, value)
            else:
                self.data[name] = value

    def __getattr__(self, name):
        if name in self.methods:
            return functools.partial(self.methods[name], self)

        if name in self.data:
            return self.data[name]

        return None

    def all(self):
        """
        return a dict with all values from the done
        """
        data = self.__dict__.copy()
        del(data['methods'])
        del(data['id'])

        for name, value in data['data'].iteritems():
            if name in data:
                raise InvalidDataException("duplicate key %s: node.%s and node.data['%s']" % (name, name, name))

            data[name] = value

        return data

class NodeContext(object):
    def __init__(self, node, settings=None):
        self.node = node
        self.settings = settings or {}

    def __getattr__(self, name):
        if name in self.settings:
            return self.settings[name]

        return None