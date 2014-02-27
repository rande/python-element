Api
===

Features
--------

  - Expose node from the datasource through a RESTful API.

Configuration
-------------

You need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.api:

Then, you must have a node api as defined in your datasource:

.. code-block:: yaml

    # api.yml
    title: API
    type: action.collection
    actions:
        element_api_node:
            path: /element/node/<path:path>.<_format>
            methods: ['GET', 'PUT', 'POST', 'DELETE']
            defaults:
                _controller: element.api.view.node:execute

        element_api_list_index:
            path: /element/node.<_format>
            methods: ['GET']
            defaults:
                _controller: element.api.view.node.list:execute
                path: /

        element_api_list:
            path: /element/path/<path:path>.<_format>
            methods: ['GET']
            defaults:
                _controller: element.api.view.node.list:execute

        element_api_handler_list:
            path: /element/handlers.<_format>
            methods: ['GET']
            defaults:
                _controller: element.api.view.handler.list:execute

        element_api_handler:
            path: /element/handler/<code>.<_format>
            methods: ['GET']
            defaults:
                _controller: element.api.view.handler:execute


.. note::

    The API is not stable.

Usage
-----

 - ``GET /api/element/handlers.json`` : return the list of handlers
 - ``GET /api/element/node.json``: return the different node available
 - ``GET /api/element/node/{ID}.json``: get a node
 - ``POST /api/element/node/{ID}.json``: update a node
 - ``PUT /api/element/node/{ID}.json``: create a node
