

class ErrorListener(object):
    def __init__(self, node_manager, renderer):
        self.node_manager = node_manager
        self.renderer = renderer

    def handle_400_error(self, event):
        return self.handle('errors/40x', event)

    def handle_500_error(self, event):
        return self.handle('errors/50x', event)

    def handle(self, path, event):
        node = self.node_manager.get_node(path)

        if not node or not event.has('request_handler'):
            return

        self.renderer.render(event.get('request_handler'), node)