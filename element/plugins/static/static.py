import element.node
import os

class StaticHandler(element.node.NodeHandler):
    def __init__(self, base_dir, templating):
        self.base_dir = base_dir
        self.templating = templating

    def get_defaults(self, node):
        return {}

    def get_name(self):
        return 'Static'

    def execute(self, request_handler, context):
        if not context.mode or context.mode == 'raw':
            file = os.path.realpath(context.node.file)

            if file[:len(self.base_dir)] != self.base_dir:
                request_handler.set_status(404)

            request_handler.send_file(file)

        if context.mode == "preview":
            params = {
                'context': context
            }

            self.render(request_handler, self.templating, 'element.plugins.static:preview.html', params)
