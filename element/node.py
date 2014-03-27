import yaml, os, functools
from element.manager import generate_uuid
import datetime
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
            nodes.append(Node(data['uuid'], data))

        event = self.event_dispatcher.dispatch('element.nodes.load.success', {
            'nodes': nodes
        })

        return event.get('nodes')

    def get_node(self, uuid):
        if self.logger:
            self.logger.debug('NodeManager.get_node: %s' % uuid)

        if isinstance(uuid, Node):
            return uuid

        # clean up this ... not perfect at all...
        try:
            data = self.db.retrieve(uuid)
        except Exception, e:
            if self.logger:
                self.logger.debug('NodeManager.get_node: %s ~ exception: %s' % (uuid, e.message))

            data = None

            # raise e

        if not data:
            if self.logger:
                self.logger.debug('NodeManager.get_node: %s ~ cannot find node with uuid, looking for alias' % uuid)

            data = self.db.find_one(alias="/%s" % uuid)

        # always assume a fail
        event_name = 'element.node.load.fail'
        params = {'uuid': uuid}

        if data:
            if self.logger:
                self.logger.debug('NodeManager.get_node: %s ~ Found! ~ %s' % (uuid, data))

            event_name = 'element.node.load.success'
            params = {
                'node': Node(uuid, data)
            }

        else:
            if self.logger:
                self.logger.debug('NodeManager.get_node: %s ~ Not Found!' % uuid)

        event = self.event_dispatcher.dispatch(event_name, params)

        if event.has('node'):
            return event.get('node')

        return None

    def delete(self, node):
        self.event_dispatcher.dispatch('element.node.pre_delete', {
            'node': node,
        })

        result = self.db.delete(node.uuid)

        self.event_dispatcher.dispatch('element.node.post_delete', {
            'node': node,
        })

        return result
        
    def save(self, node):
        event = self.event_dispatcher.dispatch('element.node.pre_save', {
            'node': node,
            'data': node.data
        })

        result = self.db.save(node.uuid, event.get('node').all())

        self.event_dispatcher.dispatch('element.node.post_save', {
            'node': node,
            'data': node.data
        })

        return result

    def get_handler(self, node):
        return self.handlers[node.type]

class Node(object):
    def __init__(self, uuid=None, data=None):

        self.methods = {}
        self.uuid = uuid or generate_uuid()

        self.manager = None
        # set default values

        self.id = None
        self.path = None
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

        self.define(data)

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

        for name, value in data['data'].iteritems():
            if name in data:
                raise InvalidDataException("duplicate key %s: node.%s and node.data['%s']" % (name, name, name))

            data[name] = value

        del(data['data'])

        return data

    def define(self, data):
        self.data = {}

        for name, value in data.iteritems():
            if name == 'uuid':
                continue

            if name in self.__dict__:
                self.__setattr__(name, value)
            else:
                self.data[name] = value


class NodeContext(object):
    def __init__(self, node, settings=None):
        self.node = node
        self.settings = settings or {}

    def __getattr__(self, name):
        if name in self.settings:
            return self.settings[name]

        return None