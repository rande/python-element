from element.plugins.security.exceptions import AuthenticationCredentialsNotFoundException

class Token(object):
    pass

class AnonymousToken(Token):
    def __init__(self, key, user, roles=None):
        self.key = key
        self.user = user
        self.roles = roles or []

class SecurityContext(object):
    def __init__(self):
        self.token = None

    def is_granted(self, attributes, object=None):
        # simple implementation for now

        if not self.token: 
            raise AuthenticationCredentialsNotFoundException("No token attached to the security token")

        if not isinstance(attributes, list):
            attributes = [attributes]

        if len(attributes) == 0:
            return False

        for attribut in attributes:
            if attribut not in self.token.roles:
                return False

        return True

