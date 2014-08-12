#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from element.plugins.security.exceptions import AuthenticationException, \
    AccountStatusException, ProviderNotFoundException, \
    UsernameNotFoundException, AuthenticationServiceException, \
    BadCredentialsException

from element.plugins.security.security import UsernamePasswordToken

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
        return isinstance(token, UsernamePasswordToken) and token.key == self.provider_key

    def authenticate(self, token):
        if not self.supports(token):
            return

        try:
            user = self.user_provider.loadUserByUsername(token.username)

            if user.password != token.credentials:
                raise BadCredentialsException('Invalid credentials, check login or password')

            token = UsernamePasswordToken(token.key, user, roles=user.roles)
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
