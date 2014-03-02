Seo
===

Features
--------

  - Alter node to include SEO information

Configuration
-------------

You need to enable the module ``element.plugins.seo`` and configure the ``title_pattern`` setting.

.. code-block:: yaml

    element.plugins.seo:
        title_pattern: "%seo.title_pattern%"

Events
------

 - The plugin is registered to the ``element.node.load.success`` event to add SEO information.

