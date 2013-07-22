

class ErrorListener(object):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def handle_400_error(self, event):
        return self.handle('errors/40x', event)

    def handle_500_error(self, event):
        return self.handle('errors/50x', event)

    def handle(self, path, event):
        node = self.node_manager.get_node(path)

        if not node: return

        node.response['status_code'] = event.get('status_code')

        event.set('node', node)
