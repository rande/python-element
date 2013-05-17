import ioc.event
import dateutil.parser
import datetime

class Standardize(object):
    def normalize_node(self, event):
        node = event.get('node')
        self.normalize(node)

    def normalize_nodes(self, event):
        for node in event.get('nodes'):
            self.normalize(node)

    def normalize(self, node):
        """
        Normalize node to make sure the default fields are set properly
        """
        
        if 'created_at' not in node.data or not node.data['created_at']:
            node.data['created_at'] = datetime.datetime.now()

        if not isinstance(node.data['created_at'], datetime.datetime):
            node.data['created_at'] = dateutil.parser.parse(node.data['created_at'])

        if 'published_at' not in node.data or not node.data['published_at']:
            node.data['published_at'] = datetime.datetime.now()

        if not isinstance(node.data['published_at'], datetime.datetime):
            node.data['published_at'] = dateutil.parser.parse(node.data['published_at'])

        if 'enabled' not in node.data:
            node.data['enabled'] = True

        if 'content' not in node.data:
            node.data['content'] = False

        if 'title' not in node.data:
            node.data['title'] = "No title defined"

        if 'tags' not in node.data:
            node.data['tags'] = []

        if 'category' not in node.data:
            node.data['category'] = False

        if 'response' not in node.data:
            node.data['response'] = {}

        defaults = {
            'Cache-Control': [
                'no-cache'
            ],
        }

        defaults.update(node.data['response'])

        node.data['response'] = defaults


    def render_response(self, event):
        pass