Architecture
============

Definitions
~~~~~~~~~~~

* ``node``: the smallest data available, it represents a content stored into the datastore. A node must contain
    * ``id``:   the internal identifier used by the datasource
    * ``path``: the path to reach the node, the path is the external identifier to the node
    * ``data``: a dictionary of key-value representing the content
    * ``type``: the node type, the node type will be used to handle the node
    * ``manager``: the manager code which handle this node
    * ``created_at``
    * ``published_at``
    * ``enabled``
    * ``content``
    * ``title``
    * ``tags``
    * ``category``
    * ``copyright``
    * ``authors``

* ``node handler``: it is a service used to render a node, there is one service per node type.

Components used
~~~~~~~~~~~~~~~

* ``python 2.7``: the main python version supported for now
* ``IoC``: it is a dependency container used to handle Element configuration and to instantiate all required services
* ``Tornado``: it is used to handle request and render response, Element also register custom routes to render nodes.
* ``jinja``: render templates.
* ``unittest2``: used to test the framework
* ``mongodb``: the main datastore for the content.


Application bootstrapping
~~~~~~~~~~~~~~~~~~~~~~~~~

The project used IoC to handle configuration, the skeleton application demonstrates some of its usage. The configuration files
are stored in the ``config`` folder. The configuration is split into several files (this is not mandatory), each files have
its own configuration:

* ``config.yml``: this file contains the main configuration: module to load and shared parameters.
* ``parameters_*.yml``: some parameters are only used on some environments, so depends on those parameters the application
  might behave differently (use different datastore, or webservice's credentials)
* ``services.yml``: this file can contains your own custom services

.. note::

    This configuration layout is not mandatory, you can organize those files as you want. Just alter the start.py file
    in order to match your wishes.

There are 2 ways to use the application:

* ``command line``: expose commands to produce or alter data
* ``web``: expose the data to the client.

The command line and the web does not use the same application instance. so make sure every thing is stateless.

Events
~~~~~~

Most of the code is created using event to increase flexibility with how an user can interact with the ``Python Element``.
Some events are explained in the next section, other events are available on the :doc:`dedicated documentation</events>` .


Request / Response workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* rewrite this part to explain tornado usage

Plugins
-------

Every things is a plugin, if you don't like a feature just don't enable the plugin and create your own plugin!

You can view current internal plugin in the :doc:`plugins section</plugins>`

Bower
-----

Elements relies on ``bower`` to install assets. All plugins use the base path ``resources/static/vendor`` to declare
assets. So you should/must configure your ``.bowerrc`` like this.

.. code-block:: json

    {
        "directory": "resources/static/vendor"
    }
