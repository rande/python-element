import os, yaml
import element

class NodeLoader(object):
    pass

class LoaderChain(NodeLoader):
    def __init__(self):
        self.loaders = {}

    def add_loader(self, name, loader):
        self.loaders[name] = loader

    def supports(self, id):
        return True

    def load(self, data):
        for name, loader in self.loaders.iteritems():
            if not loader.supports(data):
                continue

            return loader.load(data)

class YamlNodeLoader(NodeLoader):
    """
    Load a node by using a yaml definition
    """
    def supports(self, path):
        return path[-3:] == 'yml' and os.path.isfile(path)

    def load(self, path):
        return yaml.load(open(path, 'r'))

class InlineLoader(NodeLoader):
    """
    Load a node from content provided
    """
    def supports(self, node):
        return isinstance(node, dict) and 'type' in node and 'id' in node

    def load(self, node):
        return node
