from . import EntryPoint, SecurityFactory
from ioc.component import Reference, Definition
from element.plugins.security.security import UsernamePasswordToken
from element.plugins.security.exceptions import AuthenticationException


class BasicAuthEntryPoint(EntryPoint):
    def __init__(self, realmName, logger=None):
        self.realmName = realmName
        self.logger = logger

    def start(self, request):
        import flask

        response = flask.make_response('', 401)
        response.headers['WWW-Authenticate'] = 'Basic realm="%s"' % self.realmName

        return response

class BasicAuthenticationListener(object):
    AUTHORIZATION_HEADERS = [
        'HTTP_AUTHORIZATION',
        'REDIRECT_HTTP_AUTHORIZATION'
    ]

    def __init__(self, provider_key, security_context, entry_point, authentication_manager, logger=None):
        self.provider_key = provider_key
        self.security_context = security_context
        self.entry_point = entry_point
        self.authentication_manager = authentication_manager
        self.logger = logger

    def handle(self, event):
        request = event.get('request')

        # check the current token
        token = self.security_context.token

        if token and token.authenticated and token.username == request.authorization.username:
            self.logger.info("BasicAuthenticationListener - token is valid")
            return

        if not request.authorization:
            self.logger.info("BasicAuthenticationListener - no authorization headers, sending default one")

            self.security_context.token = None
            event.set('response', self.entry_point.start(request))

            return

        # no token, create a new one and check credential
        try:
            token = UsernamePasswordToken(self.provider_key, request.authorization.username)
            token.credentials = request.authorization.password
            token = self.authentication_manager.authenticate(token)
            
            self.security_context.token = token

            if self.logger:
                self.logger.info("BasicAuthenticationListener - AuthenticationException OK")

        except AuthenticationException, e:
            self.security_context.token = None
            event.set('response', self.entry_point.start(request))

            if self.logger:
                self.logger.info("BasicAuthenticationListener - AuthenticationException occurs : %s" % e)


class HttpBasicSecurityFactory(SecurityFactory):
    def __init__(self):
        self.position = "http"
        self.key = "http_basic"

    def create(self, container_builder, id, config):
        auth_provider_id = "element.plugins.security.auth.basic.auth_provider.%s" % id
        auth_provider = container_builder.create_definition('element.plugins.security.auth.auth_provider')
        auth_provider.arguments[0] = Reference(config.get('provider'))
        auth_provider.arguments[1] = id

        container_builder.add(auth_provider_id, auth_provider)

        entry_point_id = "element.plugins.security.auth.basic.entry_point.%s" % id
        entry_point = container_builder.create_definition('element.plugins.security.auth.basic.entry_point')
        entry_point.arguments[0] = config.get("realm_name")

        container_builder.add(entry_point_id, entry_point)

        handler_id = 'element.plugins.security.auth.basic.handler.%s' % id
        handler = container_builder.create_definition('element.plugins.security.auth.basic.handler')
        handler.arguments[0] = id
        handler.arguments[2] = Reference(entry_point_id)

        container_builder.add(handler_id, handler)

        return auth_provider_id, handler_id, entry_point_id
