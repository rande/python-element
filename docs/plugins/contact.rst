Contact
=======

Features
--------

  - Add a simple contact form as a block

Configuration
-------------

You need to enable the module ``ioc.extra.mailer`` and configure the smtp settings.

.. code-block:: yaml

    ioc.extra.mailer:
        host:       smtp.localhost
        port:
        user:
        password:

Usage
-----

Create a ``contact.form`` node:

.. code-block:: yaml

    # /contact.yml
    title: Contact
    type: contact.form
    email:
        to:        an-email@localhost
        from:      'no-reply@localhost'
        subject:   'Contact Form localhost'