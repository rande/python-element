import element.handlers.node

class RssHandler(element.handlers.node.IndexHandler):

    def get_base_template(self):
        return 'element:handlers/feed/index.rss'