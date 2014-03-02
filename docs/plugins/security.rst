Security
========

Features
--------

  - Add security and access control to your application
  - The current implementation is based on the `Security Component`_ from the Symfony2 framework.

.. note::

    For now, there is only one authentication implemented: the http basic.

Configuration
-------------

There is no configuration option. You only need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.security:
        role_hierarchy:
            ROLE_PUBLIC:      [IS_AUTHENTICATED_ANONYMOUSLY]
            ROLE_ADMIN:       [ROLE_PUBLIC, ROLE_USER]

        providers:
            in_memory:
                users:
                    - {'username': 'admin', 'password': 'admin', roles: ['ROLE_ADMIN']}

        firewalls:
            private:
                pattern:            ^/(admin|api)(.*)
                http_basic:
                    provider:       element.plugins.security.provider.in_memory
                    # login_path:     /admin/login
                    # use_forward:    false
                    # check_path:     /admin/login_check
                    # failure_path:   null
                # logout:
                    # path:           /admin/logout
                anonymous:          false  # allow anonymous connection

            public:
                pattern:            "^/.*"
                anonymous:          true    # allow anonymous connection

        access_control:
            - { path: ^/admin/login$,       role: IS_AUTHENTICATED_ANONYMOUSLY }
            - { path: ^/admin/logout$,      role: IS_AUTHENTICATED_ANONYMOUSLY }
            - { path: ^/admin/login-check$, role: IS_AUTHENTICATED_ANONYMOUSLY }
            - { path: ^/(admin|api),        role: ROLE_ADMIN }
            - { path: ^/.*,                 role: ['IS_AUTHENTICATED_ANONYMOUSLY'] }



.. _Security Component:: http://symfony.com/doc/current/book/security.html