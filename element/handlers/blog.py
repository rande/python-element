import markdown, os
import element.handlers
import datetime

class IndexHandler(element.handlers.NodeHandler):
    def __init__(self, node_manager):
        self.node_manager = node_manager
        
    def get_defaults(self, node):
        return {
            'template': 'handlers/blog/index.html'
        }

    def execute(self, context, flask):
        # lfrom = len(self.data_dir) + 1

        now = datetime.datetime.now()

        nodes = self.node_manager.get_nodes(path=context.node.id, type='blog.post', selector=lambda node: now > node.published_at)

                # if root[lfrom - 1:] == context.node.id:
                #     continue

                # node = self.node_manager.get_node("%s/%s" % (root[lfrom:], f[:-4]))

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
