Angular Admin
=============

The plugin provides an AngularJS Admin to edit contains

Configuration
-------------

There is no configuration option. You only need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.ngadmin:

Usage
-----

You can access to the admin using the url ``/element/static/element.plugins.ngadmin/index.html``. You can create a redirect node to make the url a bit shorter:

.. code-block:: yaml

    # /admin.yml
    type: action.redirect
    redirect: /element/static/element.plugins.ngadmin/index.html


.. note::

    The ngadmin plugin will be refactored ;)

