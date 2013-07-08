import element.handlers
import element.node

import os

class StaticHandler(element.handlers.NodeHandler):
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def get_defaults(self, node):
        return {}

    def execute(self, context, flask):

        if not context.mode or context.mode == 'raw':
            file = os.path.realpath(context.node.file)

            if file[:len(self.base_dir)] != self.base_dir:
                flask.abort(404)

            return flask.send_file(file, mimetype=context.node.mimetype)

        if context.mode == "preview":
            params = {
                'context': context
            }
            
            return flask.make_response(flask.render_template('element:handlers/static/preview.html', **params))    
