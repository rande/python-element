Cache
=====

Features
--------

  - The plugins add support for altering cache information on the response

Configuration
-------------

You need to enable the plugin by adding the ``element.plugins.cache`` module and defines a set of ``cache_control`` entries.

.. code-block:: yaml

    element.plugins.cache:
        cache_control:
            - { "path": "^.*\\.(txt|jpg|png|gif|xls|doc|docx)$",    "Cache-Control": ['public', 's-maxage=14212800']}
            - { "path": "^(blog|gallery).*",    "Cache-Control": ['public', 's-maxage=3600']}
            - { "path": "^.*\\.rss",            "Cache-Control": ['public', 's-maxage=3600']}
            - { "path": "^contact.*",           "Cache-Control": ['private', 'must-revalidate']}
            - { "path": "^/$",                  "Cache-Control": ['public', 's-maxage=3600']}

A cache entry defines:
 - ``path``: a regular expression to find the rule that should be applied.
 - ``Cache-Control``: the data to append to the response

By default, if no match is found then the Cache-Control value will be ``private, must-revalidate``

Architecture
------------

 - The plugin listen to the ``element.node.render_response`` event.
