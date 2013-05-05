import os, yaml
import element

class NodeLoader(object):
    pass

class YamlNodeLoader(NodeLoader):
    """
    Load a node by using a yaml definition
    """
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def supports(self, id):
        return os.path.isfile(self.get_id(id))

    def load(self, id):
        node = yaml.load(open(self.get_id(id), 'r'))

        return element.node.Node(
            id,
            node['type'] if 'type' in node else None,
            node,
        )

    def get_id(self, id):
        path = "%s/%s.yml" % (self.data_dir, id)

        if os.path.isfile(path):
            return path

        return "%s/%s/_index.yml" % (self.data_dir, id) 

class InlineLoader(NodeLoader):
    """
    Load a node from content provided
    """
    def supports(self, node):
        return isinstance(node, dict) and 'type' in node and 'id' in node

    def load(self, node):
        return element.node.Node(
            node['id'],
            node['type'],
            node,
        )
