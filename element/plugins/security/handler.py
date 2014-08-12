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

from .security import AnonymousToken, UsernamePasswordToken
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
    def __init__(self, map, security_context, role_hierarchie, logger=None):
        self.map = map
        self.logger = logger
        self.security_context = security_context
        self.role_hierarchie = role_hierarchie

    def handle(self, event):
        if not self.security_context.token:
            raise AuthenticationCredentialsNotFoundException("No token attached to the security token (AccessMapListener)")

        if not event.has('request'):
            raise NoRequestFoundException()

        required_roles = self.map.get_pattern(event.get('request'))

        if not required_roles:
            raise AccessDeniedException()

        user_roles = list(set(self.role_hierarchie.get_reachable_roles(self.security_context.token.roles) + self.security_context.token.roles))

        for role in required_roles:
            if role not in user_roles:
                raise AccessDeniedException()

        if self.logger:
            self.logger.info("AccessMapListener - token allowed to access the request resource")


class ContextHandler(object):
    def __init__(self, security_context, user_provider, context_name, logger=None):
        self.security_context = security_context
        self.user_provider = user_provider
        self.context_name = context_name
        self.logger = logger

    def handle(self, event):
        pass

class TornadoContextHandler(ContextHandler):
    def handle(self, event):
        """
        Load the token from the user token
        """

        name = "_security_%s" % self.context_name

        data = event.get('request_handler').get_secure_cookie(name)

        if self.logger:
            self.logger.info("TornadoContextHandler - Trying to load %s from session" % name)

        # retrieve the token from the session
        if not data:
            self.security_context.token = None

            if self.logger:
                self.logger.info("TornadoContextHandler - No data in session for key %s" % name)

            return

        token = pickle.loads(data)

        # always reload the user from the datasource
        if isinstance(token, UsernamePasswordToken):
            user = self.user_provider.loadUserByUsername(token.username)
            token.user = user

        # update the token
        self.security_context.token = token

        if self.logger:
            self.logger.info("TornadoContextHandler - token has been set to the SecurityContext")

    def handleResponse(self, event):
        """
        Save the token into the current user session
        """

        if not self.security_context.token:
            if self.logger:
                self.logger.info("TornadoContextHandler - Cannot save: no token associated")

            return

        if self.security_context.token.key != self.context_name:
            if self.logger:
                self.logger.info("TornadoContextHandler - Cannot save: current active token (%s) is not associated to the current context (%s)",
                    self.security_context.token.key,
                    self.context_name
                )

            return

        name = "_security_%s" % self.context_name

        if self.logger:
            self.logger.info("TornadoContextHandler - Saving context %s" % name)

        event.get('request_handler').set_secure_cookie(name, pickle.dumps(self.security_context.token))

