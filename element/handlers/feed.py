import element.handlers.node

class RssHandler(element.handlers.node.IndexHandler):

    def get_base_template(self, node):
        return node.template or 'element:handlers/feed/index.rss'

    def alter_response(self, response):
        response.headers['Content-Type'] = 'application/rss+xml'


class AtomHandler(element.handlers.node.IndexHandler):

    def get_base_template(self, node):
        return node.template or 'element:handlers/feed/index.atom'

    def alter_response(self, response):
        response.headers['Content-Type'] = 'application/atom+xml'