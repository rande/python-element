Architecture
============

Definitions
~~~~~~~~~~~

* ``node``: the smallest data available, it represents a content stored into the datastore. An node must contains
    * ``id``:   the internal identifier used by the datasource
    * ``path``: the path to reach the node, the path is the external identifier to the node
    * ``data``: a dictionnary of key-value representing the content
    * ``type``: the node type, the node type will be used to handle the node

* node handler: it is a service used to render a node, there is one service per node type.

Components used
~~~~~~~~~~~~~~~

* ``python 2.7``: the main python version supported for now
* ``IoC``: it is a dependency container used to handle Element configuration and to instantiate all required services
* ``Flask``: it is used to handle request and render response, Element also register custom routes to render nodes. The jinja
 version is not the default one, the instance is handled by the IoC.
* ``unittest2``: used to test the framework
* ``mongodb``: the main datastore for the content.


Application boostrapping
~~~~~~~~~~~~~~~~~~~~~~~~

The project used IoC to handle configuration, the skeleton application demonstrates some of its usage. The configuration files
are stored in the ``config`` folder. The configuration is split into several files (this is not mandatory), each files have
its own configuration:

* ``config.yml``: this file contains the main configuration: module to load and shared parameters.
* ``parameters_*.yml``: some parameters are only used on some environments, so depends on those parameters the application
    might behave differently (use different datastore, or webservice's credentials)
* ``services.yml``: this file can contains your own custom services

.. note::

    this configuration layout is not mandatory, you can organize those files as you want. Just alter the start.py file
    in order to match your wish.

There are 2 ways to use the application:

* ``command line``: expose commands to produce or alter data
* ``web``: expose the data to the client.

The command line and the web does not use the same application instance. so make sure every thing is stateless.

Request / Response workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~

 - The wsgi wrapper (Flask application) retrieves the request information
 - Element registers a custom function to the ``before_app_request`` hook, the ioc reference is ``@element.dispatcher.request#handle``
 and the related class is ``element.event.FlaskRequestElementDispatcher``. The function generates an ``element.request``
 event where ``Element`` services can register. (This as been done to limit the usage of the Flask API.)
 If an event listener returns a response then Flask will return the response, if no response is returned then the standard
 Flask workflow is used.
 - Flask's route resolution: this step resolve the current routing and call the matching callback function.
 Element's register a route named ``element_path``, this route accepts a ``path`` argument. The route is bound to the service
 ``element.flask.view.index`` (class: element.views.PathView)
 - the PathView class retrieve the targeted node and render it by returning a ``Response`` object
 - Element registers a custom function to the ``after_app_request`` hook, the ioc reference is ``@element.dispatcher.response#handle``
 and the related class is ``element.event.FlaskResponseElementDispatcher``. The function generates an ``element.response``
 event where ``Element`` services can register.
 This feature can be used to alter the ``Response`` object (adding custom headers...)
 - The response is returned to the wsgi wrapper and then to the client

Events
~~~~~~

element.request
---------------

This event is used when a request is received by Flask. Events registered:

 - ``element.plugins.security.firewall`` : this is the security firewall used to control resource access depends on user's
 credentials and depends role required to access to the resource.

element.response
----------------

 - ``element.plugins.security.handler.FlaskContextHandler``: this is used to store security information into the user's session

