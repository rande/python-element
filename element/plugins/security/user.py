class User(object):
    def __init__(self, username, password=None, roles=None, account_non_expired=None):
        self.username = username
        self.password = password
        self.roles = roles or []


