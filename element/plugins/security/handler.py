from .security import AnonymousToken
from .exceptions import AccessDeniedException, NoRequestFoundException, AuthenticationCredentialsNotFoundException
import pickle

class AnonymousAuthenticationHandler(object):
    """
    This class generates an AnonymousToken if no token has been set in 
    the current event object
    """
    def __init__(self, key, security_context, logger=None):
        self.key = key
        self.logger = logger
        self.security_context = security_context

    def handle(self, event):   
        if self.security_context.token: 
            if self.logger:
                self.logger.info("AnonymousAuthenticationHandler - token already set, skipping")

            return

        if self.logger:
            self.logger.info("AnonymousAuthenticationHandler - creating a new AnonymousToken")

        self.security_context.token = AnonymousToken(self.key, 'anon.', ['IS_AUTHENTICATED_ANONYMOUSLY'])

class AccessMapListener(object):
    """
    This class check if the current token can access the request
    """
    def __init__(self, map, security_context, logger=None):
        self.map = map
        self.logger = logger
        self.security_context = security_context

    def handle(self, event):
        if not self.security_context.token:
            raise AuthenticationCredentialsNotFoundException("No token attached to the security token")

        if not event.has('request'):
            raise NoRequestFoundException()

        roles = self.map.get_pattern(event.get('request'))

        if not roles:
            raise AccessDeniedException()

        for role in roles:
            if role not in self.security_context.token.roles:
                raise AccessDeniedException()

        if self.logger:
            self.logger.info("AccessMapListener - token allowed to access the request resource")


class ContextHandler(object):
    def __init__(self, security_context, user_provider, context_name, logger=None):
        self.security_context = security_context
        self.user_provider = user_provider
        self.context_name = context_name
        self.logger=logger

    def handle(self, event):
        pass

class FlaskContextHandler(ContextHandler):
    def handle(self, event):
        """
        Load the token from the user token
        """
        import flask

        name = "_security_%s" % self.context_name

        if self.logger:
            self.logger.info("FlaskContextHandler - Trying to load %s from session" % name)

        # retrieve the token from the session
        if name not in flask.session:
            self.security_context.token = None

            if self.logger:
                self.logger.info("FlaskContextHandler - No data in session for key %s" % name)

            return

        token = pickle.loads(flask.session[name])

        # always reload the user from the datasource
        user = self.user_provider.loadUserByUsername(token.username)

        token.user = user

        # update the token
        self.security_context.token = token

        if self.logger:
            self.logger.info("FlaskContextHandler - token has been set to the SecurityContext")

    def handleResponse(self, event):
        """
        Save the token into the current user session
        """
        import flask


        if not self.security_context.token:
            if self.logger:
                self.logger.info("FlaskContextHandler - Cannot save: no token associated")

            return

        if self.security_context.token.key != self.context_name:
            if self.logger:
                self.logger.info("FlaskContextHandler - Cannot save: current active token is not associated to the current context")

            return

        name = "_security_%s" % self.context_name

        if self.logger:
            self.logger.info("FlaskContextHandler - Saving context %s" % name)

        # save the token into the session
        if name in flask.session:
            del flask.session[name]

        flask.session[name] = pickle.dumps(self.security_context.token)

