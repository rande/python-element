Feed
====

Features
--------

  - Add a handler to render atom/rss feed from query

Configuration
-------------

There is no configuration option. You only need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.feed:

Usage
-----

To create an atom feed, just define a node ``element.feed.atom``

.. code-block:: yaml

    # /feeds/python.atom.yml
    title: Python Feeds
    type: element.feed.atom
    filters:
        types:      [blog.post]
        tags:       [python]

To create a RSS feed, just define a node ``element.feed.rss``

.. code-block:: yaml

    # /feeds/python.rss.yml
    title: Python Feeds
    type: element.feed.rss
    filters:
        types:      [blog.post]
        tags:       [python]


If you want to create an index of feed, just create a simple index:

.. code-block:: yaml

    # /feeds/_index.yml
    title: Feeds List
    type: node.index
    template: element.plugins.node:index.html
    filters:
        types: [element.feed.rss, element.feed.atom]
        path: /feeds