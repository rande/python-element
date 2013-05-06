import ioc.event
import dateutil.parser
import datetime

class Standardize(object):
    def normalize_node(self, event):
        """
        Normalize node to make sure the default fields are set properly
        """
        node = event.get('node')

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

        if 'response' not in node.data:
            node.data['response'] = {}

        defaults = {
            'status_code': 200,
            'Cache-Control': [
                'no-cache'
            ],
        }

        defaults.update(node.data['response'])

        node.data['response'] = defaults

    def render_response(self, event):
        event.get('response').status_code = event.get('context').node.response['status_code']