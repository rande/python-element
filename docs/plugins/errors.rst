Errors
======

Features
--------

  - Return a valid error node

Configuration
-------------

There is no configuration option. You only need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.errors:

Usage
-----

Depends on the error type, the listener will look for
- ``errors/40x`` node if a node does not exist
- ``errors/50x`` node if there is an internal error

A node can be anything, here an example:

.. code-block:: yaml

    # /errors/40x.yml
    title: Page Not Found
    type: page.default
    format: markdown
    content: |
        The requested URL was not found on the server.

        If you entered the URL manually please check your spelling and try again.

Events
------

 - The plugin listen to two events: ``element.node.not_found`` and ``element.node.internal_error``

