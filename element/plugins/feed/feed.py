from element.plugins.node import node

class RssHandler(node.IndexHandler):

    def get_name(self):
        return 'RSS Feed'

    def get_base_template(self, node):
        return node.template or 'element.plugins.feed:index.rss'

    def alter_response(self, response):
        response.headers['Content-Type'] = 'application/rss+xml'


class AtomHandler(node.IndexHandler):

    def get_name(self):
        return 'Atom Feed'

    def get_base_template(self, node):
        return node.template or 'element.plugins.feed:index.atom'

    def alter_response(self, response):
        response.headers['Content-Type'] = 'application/atom+xml'