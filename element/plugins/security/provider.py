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
