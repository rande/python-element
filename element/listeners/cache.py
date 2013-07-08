import re

class CacheControl(object):
    def __init__(self, rules=None):
        self.rules = rules or []

    def cache_control(self, event):
        response = event.get('response')
        request = event.get('request')
        context = event.get('context')

        if request.method in ["GET", "HEAD"]:
            rule = self.find_rule(context.node)
        else:
            rule = self.get_default()

        response.headers['Cache-Control'] = ", ".join(rule['Cache-Control'])

    def find_rule(self, node):
        for rule in self.rules:
            if rule['path'].match(node.id):
                return rule

        return self.get_default()

    def get_default(self):
        return {
            'Cache-Control': ['private', 'must-revalidate']
        }