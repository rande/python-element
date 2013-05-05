import markdown, os
import element.handlers

class IndexHandler(element.handlers.NodeHandler):
    def __init__(self, node_manager, data_dir):
        self.node_manager = node_manager
        self.data_dir     = data_dir

    def get_defaults(self, node):
        return {
            'template': 'handlers/blog/index.html'
        }

    def execute(self, context, flask):
        nodes = []

        lfrom = len(self.data_dir) + 1

        for root, dirs, files in os.walk("%s/%s" % (self.data_dir, context.node.id)):
            for f in files:
                if root[lfrom - 1:] == context.node.id:
                    continue

                node = self.node_manager.get_node("%s/%s" % (root[lfrom:], f[:-4]))

                if not node or node.type != 'blog.post':
                    continue  
                else:
                    nodes.append(node)

        nodes.sort(key=lambda node: node.data['published_at'], reverse=True)

        params = {
            'context': context,
            'nodes': nodes
        }

        return flask.make_response(flask.render_template(context.settings['template'], **params))


class PostHandler(element.handlers.NodeHandler):
    
    def get_defaults(self, node):
        return {
            'template': 'handlers/blog/post.html'
        }

    def execute(self, context, flask):

        content = context.node.content
        if context.node.format == 'markdown':
            content = markdown.markdown(context.node.content)

        params = {
            'context': context, 
            'content': content,
        }

        return flask.make_response(flask.render_template(context.settings['template'], **params))
