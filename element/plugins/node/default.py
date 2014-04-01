class DefaultIndex(object):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def default_index(self, event):
        """
        Try to find the _index.yml file from the dedicated folder,
        if one is found, then no error will be throw to the user
        """
        node = self.node_manager.get_node("%s/_index" % event.get('path'))

        if not node:
            return

        event.stop_propagation()

        node.id = event.get('path')  # restore a valid id, as this one is virtual

        event.set('node', node)
