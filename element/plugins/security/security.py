from element.plugins.security.exceptions import AuthenticationCredentialsNotFoundException

class Token(object):
    def __init__(self, key, user, roles=None):
        self.key = key
        self.user = user
        self.roles = roles or []
        if isinstance(self.roles, str):
            self.roles = [self.roles]
            
        self.authenticated = False
        self.credential = None

    @property
    def username(self):
        if not isinstance(self.user, str):
            return self.user.username

        return self.user

class UsernamePasswordToken(Token):
    pass

class AnonymousToken(Token):
    pass
    
class SecurityContext(object):
    """
    This class is responsible to hold the security token. You need to inject this
    service in your class to check is the user is granted to access to a resource.

    The token must be resetted before each request.
    """
    def __init__(self, logger=None):
        self.token = None
        self.logger = logger

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

