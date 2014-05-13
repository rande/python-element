Seo
===

Features
--------

  - Add basic support for SEO information (title and metas)

Configuration
-------------

You need to enable the module ``element.plugins.seo`` and configure the settings.

.. code-block:: yaml

    element.plugins.seo:
        title_pattern: "%seo.title_pattern%"
        metas:
            name:
                keywords:             python, element, cms, markdown
                description:          Python Element by Thomas Rabaix ~ A CMS based on Tornado with a bit of "ioc"
                robots:               index, follow
                viewport:             width=device-width, initial-scale=1.0, maximum-scale=1, user-scalable=no

            property:
                # Facebook application settings
                #'fb:app_id':          XXXXXX
                #'fb:admins':          admin1, admin2

                # Open Graph information
                # see http://developers.facebook.com/docs/opengraphprotocol/#types or http://ogp.me/
                'og:site_name':       Python Element by Thomas Rabaix
                'og:description':     A CMS based on Tornado

            http-equiv:
                'Content-Type':         text/html; charset=utf-8
                #'X-Ua-Compatible':      IE=EmulateIE7


Usage
-----

You can add seo information on a node, by using a ``seo`` fields:

.. code-block:: yaml

    title: Homepage
    seo:
        title: The Python Element Homepage
        metas:
            name:
                description: Python Element by Thomas Rabaix ~ A CMS based on Tornado with a bit of "ioc" ;)

            property:
                'og:description':     A CMS based on Tornado ;)

    type: page.default
    format: markdown

    ----
    The content here


The seo information will be rendered by using the special ``render_node_event`` helper with the ``element.seo.headers`` event.

.. code-block:: jinja

    {% if context %}
        {{ render_node_event('element.seo.headers', options={'subject': context})|safe }}
    {% else %}
        {{ render_node_event('element.seo.headers')|safe }}
    {% endif %}


.. note::

    The seo information from the node will be merged with the one from the default configuration.