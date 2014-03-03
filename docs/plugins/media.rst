Media
=====

  - Display a gallery of media

Configuration
-------------

There is no configuration option. You only need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.media:

Usage
-----

You can create a gallery with this node:

.. code-block:: yaml

    # /gallery/2010/australia/_index.yml
    title: Australia
    type: media.gallery
    format: markdown
    base_template: element:base_gallery.html
    content: |
        Australia is one country where everything is possible, from dessert to the sea, from
        the walabee to the shark. This country is incredible.

