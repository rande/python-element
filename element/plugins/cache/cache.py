class CacheControl(object):
    """
    This class attach cache header to the request matching the pattern
    """

    def __init__(self, rules=None):
        self.rules = rules or []

    def cache_control(self, event):
        request_handler = event.get('request_handler')
        context = event.get('context')

        if request_handler.request.method in ["GET", "HEAD"]:
            rule = self.find_rule(request_handler.request.path)
        else:
            rule = self.get_default()

        for name, value in rule.iteritems():
            request_handler.set_header(name, ", ".join(value))

    def find_rule(self, path):
        for rule in self.rules:
            if rule['path'].match(path):
                return rule

        return self.get_default()

    def get_default(self):
        return {
            'Cache-Control': ['private', 'must-revalidate']
        }