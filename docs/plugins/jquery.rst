.. note::

    This documentation is under construction, more to come soon



JQuery
======

Features
~~~~~~~~

  - Insert here the different feature available for this plugin

Configuration
~~~~~~~~~~~~~

  - Insert the yaml configuration for the DI

.. code-block:: yaml

    element.plugins.cache:
        cache_control:
            - { "path": "^.*\\.(txt|jpg|png|gif|xls|doc|docx)$",    "Cache-Control": ['public', 's-maxage=14212800']}
            - { "path": "^(blog|gallery).*",    "Cache-Control": ['public', 's-maxage=3600']}
            - { "path": "^.*\\.rss",            "Cache-Control": ['public', 's-maxage=3600']}
            - { "path": "^contact.*",           "Cache-Control": ['private', 'must-revalidate']}
            - { "path": "^/$",                  "Cache-Control": ['public', 's-maxage=3600']}

Events
~~~~~~

 - List event or entry points for this plugin

Architecture
~~~~~~~~~~~~

 - Provide information about how the feature is implemented
