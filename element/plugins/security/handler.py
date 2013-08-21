from .security import AnonymousToken
from .exceptions import AccessDeniedException, NoRequestFoundException, AuthenticationCredentialsNotFoundException

class AnonymousAuthenticationHandler(object):
    """
    This class generates an AnonymousToken if no token has been set in 
    the current event object
    """
    def __init__(self, key):
        self.key = key

    def handle(self, event):
        if event.has('token'): 
            return

        event.data['token'] = AnonymousToken(self.key, 'anon.')

class AccessMapListener(object):
    def __init__(self, map):
        self.map = map

    def handle(self, event):
        if not event.has('token'): 
            raise AuthenticationCredentialsNotFoundException("No token attached to the security token")

        if not event.has('request'):
            raise NoRequestFoundException()

        roles = self.map.get_pattern(event.get('request'))

        if not roles:
            raise AccessDeniedException()

        for role in roles:
            if role not in event.get('token').roles:
                raise AccessDeniedException()
