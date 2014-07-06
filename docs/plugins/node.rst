Node
====

The node plugin is a core plugin as it provides main features to render a node.

Configuration
-------------

.. code-block:: yaml

    element.plugins.node:
        render_type: esi # or ssi

Usage
-----

The plugin provide a node index handler to render a list of node

.. code-block:: yaml

    # /blog/_index.yml
    title: Feeds List
    type: node.index
    template: element.plugins.node:index.html
    filters:
        types: [element.feed.rss, element.feed.atom]
        path: /feeds

The ``filters`` option accept arguments:
- ``types``: filter nodes by types
- ``category``: filter by category
- ``path``: lookup from the specified path
- ``tags``: filter nodes the provided tags
- ``limit``: limit the number of result to return
- ``offset``: set the offset

Jinja Functions
---------------

render_node_event
~~~~~~~~~~~~~~~~~

This helper allows to create a place holder inside a template where listeners can generate some contents.

A good example is a blog post where comments are required. However, the comment mechanism might not be implemented as
many solutions exist. The solution is to used the ``render_node_event`` helper to raise a specific event with proper
option like the ``subject``.

.. code-block:: jinja

    {{ render_node_event('node.comment.list', options={'subject': context.node}) }}

render_node
~~~~~~~~~~~

This helper renders a node instance.

.. code-block:: jinja

    {{ render_node(node) }}

render
~~~~~~

This helper render an ESI tag or a SSI tag. This can be useful if you want to reuse a controller. It is a valid solution
if you don't have a node to render.


.. code-block:: jinja

    {{ render(path('element_profiler_wdt', token=token, position='normal')) }}


Jinja Filters
-------------

markup
~~~~~~

This filter take a node and return a formatted string.

.. code-block:: yaml

    type: blog.post
    title: Test
    format: markdown

    ----
    ## John Doe

    Put a Resume here!!


.. code-block:: jinja

    {{ node|markup }}

Events
------

The plugin listen to two events: ``element.node.load.success`` and ``element.nodes.load.success`` for normalizing a
node. The normalization make sure that all :doc:`required fields</architecture>` are set.

