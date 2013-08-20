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
        self.map.append((rule, context))

    def get_context(self, request):
        for rule, context in self.map:
            if rule.match(request.path):
                return context

class FirewallContext(object):
    def __init__(self, listeners):
        self.listeners = listeners

    def get_context(self):
        return (self.listeners)

class Firewall(object):
    def __init__(self, map):
        self.map = map

    def onRequest(self, event):
        listeners = self.map.getListeners(event.data['request'])

        for listener in listeners:
            listener.handle(event)

            if 'response' in event.data:
                return

