class AuthenticationException(Exception):
    pass

class AccessDeniedException(Exception):
    pass
    
class UsernameNotFoundException(AuthenticationException):
    pass

class AuthenticationCredentialsNotFoundException(AuthenticationException):
    pass

class NoRequestFoundException(AuthenticationException):
    pass

class UnsupportedUserException(AuthenticationException):
    pass

class AccountStatusException(AuthenticationException):
    pass

class ProviderNotFoundException(AuthenticationException):
    pass

class BadCredentialsException(AuthenticationException):
    pass

class AuthenticationServiceException(AuthenticationException):
    pass