import ioc.event
import dateutil.parser
import datetime

def normalize_node(event):
    """
    Normalize node to make sure the default fields are set properly
    """
    node = event.get('node')

    if 'created_at' not in node.data or not node.data['created_at']:
        node.data['created_at'] = datetime.datetime.now()

    if not isinstance(node.data['created_at'], datetime.datetime):
        node.data['created_at'] = dateutil.parser.parse(node.data['created_at']).date()

    if 'published_at' not in node.data or not node.data['published_at']:
        node.data['published_at'] = datetime.datetime.now()

    if not isinstance(node.data['published_at'], datetime.datetime):
        node.data['published_at'] = dateutil.parser.parse(node.data['published_at']).date()

    if 'enabled' not in node.data:
        node.data['enabled'] = True