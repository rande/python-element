Static
======

Features
--------

  - Add a handler to render static file

Configuration
-------------

There is no configuration option. You only need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.static:

Usage
-----

Just place a store a file in the datasource and access it with a browser. That's it.

If the url contains the ``?mode=preview`` then the static will be rendered into a preview mode.


Jinja Helpers
-------------

The plugin provides 2 jinja plugins:

 - ``url_media_resize`` : take the width as parameter and generates a valid url to a resized version of the targetted media.
 - ``url_media_crop`` : take the ``size`` and the optional ``crop`` tuples to generates a valid url to a cropped version of the targetted media.

.. code-block:: jinja

    {% for media in medias %}
        <a href="{{ url_media_resize(media, 1440) }}" class="swipebox" title="{{ media.name }}">
            <img src="{{ url_media_crop(media, size=(234, 234), crop=(0.5, 0.5)) }}" alt="image" width="250px">
        </a>
    {% endfor %}

Architecture
------------

The plugin provides a ``StaticNodeLoader`` to create a node object from a path, the created node type is ``element.static``.