class CacheControl(object):
    """
    This class attach cache header to the request matching the pattern
    """

    def __init__(self, rules=None):
        self.rules = rules or []

    def cache_control(self, event):
        request_handler = event.get('request_handler')

        if request_handler.request.method in ["GET", "HEAD"]:
            values = self.find_values(request_handler.request.path)
        else:
            values = self.get_default()

        for name, value in values.iteritems():
            request_handler.set_header(name, ", ".join(value))

    def find_values(self, path):
        for rule, values in self.rules:
            if rule.match(path):
                return values

        return self.get_default()

    def get_default(self):
        return {
            'Cache-Control': ['private', 'must-revalidate']
        }