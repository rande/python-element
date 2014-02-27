Static
======

Features
--------

  - Add a handler to render static file

Configuration
-------------

There is no configuration option. You only need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.static:

Usage
-----

Just place a store a file in the datasource and access it with a browser. That's it.

If the url contains the ``?mode=preview=

Architecture
------------

The plugin provides a ``StaticNodeLoader`` to create a node object from a path, the created node type is ``element.static``.