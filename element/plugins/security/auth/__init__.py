from element.plugins.security.exceptions import AuthenticationException, \
    AccountStatusException, ProviderNotFoundException, \
    UsernameNotFoundException, AuthenticationServiceException, \
    BadCredentialsException

from element.plugins.security.security import Token

class EntryPoint(object):
    def start(self, request):
        pass

class SecurityFactory(object):
    pass

class DaoAuthenticationProvider(object):
    def __init__(self, user_provider, provider_key):
        self.user_provider = user_provider
        self.provider_key = provider_key

    def supports(self, token):
        return token.key == self.provider_key

    def authenticate(self, token):
        if not self.supports(token):
            return

        try:
            user = self.user_provider.loadUserByUsername(token.username)

            if user.password != token.credentials:
                raise BadCredentialsException('Invalid credentials, check login or password')

            token = Token(token.key, user, roles=user.roles)
            token.authenticated = True

            return token
        except UsernameNotFoundException, e:
            raise e
        
        except Exception, e:
            raise e

        if not user:
            raise UsernameNotFoundException()

class AuthenticationProviderManager(object):
    def __init__(self, event_dispatcher, auth_providers):
        self.event_dispatcher = event_dispatcher
        self.auth_providers = auth_providers

    def authenticate(self, token):
        result = None
        lastException = None

        for provider in self.auth_providers:
            if not provider.supports(token):
                continue

            try:
                result = provider.authenticate(token)
                if result:
                    break

            except AccountStatusException, e:
                e.token = token

                raise e

            except AuthenticationException, e:
                lastException = e

        if result:
            return result

        if not lastException:
            lastException = ProviderNotFoundException('No Authentication Provider found for token of class "%s".' % token)

        lastException.token = token

        raise lastException
