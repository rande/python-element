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

from element.plugins.security.user import User
from element.plugins.security.exceptions import UsernameNotFoundException

class BaseProvider(object):
    def loadUserByUsername(self, username):
        pass

    def refreshUser(self, user):
        pass

    def supportsClass(self, klass):
        pass

class InMemoryProvider(BaseProvider):
    def __init__(self, users=None, logger=None):
        users = users or []

        self.users = {}
        for user in users:
            self._add_user(user)

        self.logger = logger

    def _add_user(self, user):
        l = lambda k, a: a[k] if k in a else None

        self.users[user['username']] = User(
            user['username'],
            password=l('password', user),
            roles=l('roles', user),
        )
        
    def loadUserByUsername(self, username):
        if self.logger:
            self.logger.info('Firewall/InMemoryProvider - load user : %s' % username)

        if username not in self.users:
            raise UsernameNotFoundException('Username "%s" does not exist.' % username)

        return self.users[username]

    def refreshUser(self, user):
        if self.logger:
            self.logger.info('Firewall/InMemoryProvider - refresh user : %s' % user.username)

        return self.loadUserByUsername(user.username)

    def supportClass(self, klass):
        return klass == User
