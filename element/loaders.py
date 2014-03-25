import os, yaml
import element

class NodeLoader(object):
    pass

class LoaderChain(NodeLoader):
    def __init__(self, loaders=None):
        self.loaders = {}
        for loader in loaders or []:
            self.add_loader(loader[0], loader[1])

    def add_loader(self, name, loader):
        self.loaders[name] = loader

    def supports(self, id):
        return True

    def save(self, path, data):
        for name, loader in self.loaders.iteritems():
            if not loader.supports(data):
                continue

            return loader.save(path, data)

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
        if isinstance(path, dict):
            return 'type' in path and path['type'] != 'element.static'

        return path[-3:] == 'yml' and os.path.isfile(path)

    def load(self, path):
        return yaml.load(open(path, 'r'))

    def save(self, path, data):
        yaml.safe_dump(data, file(path, 'w'), 
            canonical=False,
            encoding='utf-8',
            allow_unicode=True
        )

        return True

class InlineLoader(NodeLoader):
    """
    Load a node from content provided
    """
    def supports(self, node):
        return isinstance(node, dict) and 'type' in node and 'id' in node

    def load(self, node):
        return node

    def save(self, id, data):
        return False