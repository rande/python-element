from .exceptions import AccessDeniedException

class AccessMap(object):
    def __init__(self, map=None):
        map = map or []

        self.map = []
        for rule, roles in map:
            self.add(rule, roles) 

    def add(self, rule, roles=None):
        if isinstance(roles, str):
            roles = [roles]

        self.map.append((rule, roles or []))

    def get_pattern(self, request):
        for rule, roles in self.map:
            if rule.match(request.path):
                return roles

class FirewallMap(object):
    def __init__(self, map=None):
        map = map or []
        self.map = []
        for rule, context in map:
            self.add(rule, context) 

    def add(self, rule, context):
        if not isinstance(context, tuple):
            context = (context, None)

        self.map.append((rule, context))

    def get_context(self, request):      
        for rule, context in self.map:
            if rule.match(request.path):
                return context

        return ([], None)

class Firewall(object):
    def __init__(self, map, logger=None):
        self.map = map
        self.logger = logger

    def onRequest(self, event):
        if self.logger:
            self.logger.info('Firewall - filtering request')

        request_handler = event.get('request_handler')

        listeners, options = self.map.get_context(request_handler.request)

        if len(listeners) == 0:
            if self.logger:
                self.logger.info('Firewall - no listeners found for request: %s' % event.data['request'].path)

            raise AccessDeniedException()

        if self.logger:
            self.logger.info('Firewall - found listeners %s' % listeners)

        for listener in listeners:
            listener.handle(event)

            if request_handler.is_finish():
                if self.logger:
                    self.logger.info('Firewall - listener %s generates a response' % listener)

                return

        if self.logger:
            self.logger.info('Firewall - request valid!')

