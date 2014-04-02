class Meta(object):
    def __init__(self, klass, node_type):
        self.klass = klass
        self.node_type = node_type
        self.methods = {}

class Manager(object):
    def __init__(self):
        self.collection = MetaCollection

class MetaCollection(object):
    def __init__(self):
        self.metas = {}

    def add(self, meta):
        self.metas[meta.node_type] = meta

class MetaListener(object):
    def __init__(self, collection):
        self.collection = collection

    def on_load(self, node):
        if node.type not in self.collection.metas:
            return

        node.__class__ = self.collection.metas[node.type].klass

    def on_node_load(self, event):
        self.on_load(event.get('node'))

    def on_nodes_load(self, event):
        for node in event.get('nodes'):
            self.on_load(node)