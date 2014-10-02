Presentation
============

Features
--------

  - Expose some presentation nodes (shower, slideshare, raw mode)

Configuration
-------------

There is no configuration option. You only need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.presentation:


Bower configuration
~~~~~~~~~~~~~~~~~~~

You need to install ``shower`` or/and ``reveal.js``, open your bower.json file and add

.. code-block:: json

    "dependencies": {
        "shower": "~1",
        "reveal.js": "2.6.2"
    }

Shower Presentation
-------------------

A shower presentation is defined by ``presentation.shower`` node type:

.. code-block:: yaml

    # /blog/2009/sept/18/are-my-services-coool.yml
    type: presentation.shower
    title: How to create a good presentation ?
    abstract: Let's try to show off with shower!
    published_at: 20 May 2014 12:37:48
    theme: ribbon # or bright

    ----
    class: shout

    ## The presentation
    ----
    ## Slide 1

    - My bullet point 1
    - My bullet point 2

    ----
    ## Slide 2

    - My bullet point 1
    - My bullet point 2

    ----
    ### etc ..

    ...

You can use some metadata to get better support from the theme

- ``class``:
    - ``shout``: one big title
    - ``shout grow``: a growing big title
    - ``shout shrink``: a shrinking bit title
    - ``cover``: a title + a picture
- ``id``: an html id that you can used to define custom slide
- ``data-timing``: a timer before switching to the next slide (value format: ``00:03``, ie 3s)

You can also include some stylesheet to tweak some slides

.. code-block:: text

    class: cover
    id: cover

    <style>
    #cover h2 {
        margin: 30px 0px 0px;
        color: #FFF;
        text-align: center;
        font-size: 70px;
    }

    #cover p {
        margin: 10px 0px 0px;
        text-align: center;
        color: #FFF;
        font-style: italic;
        font-size: 20px;
    }

    </style>

    ## Shower Presentation Engine

    Integrated into Python Element

    <img src="http://shwr.me/pictures/cover.jpg" />

Reveal.js Presentation
----------------------

A shower presentation is defined by ``presentation.reveal`` node type:

.. code-block:: yaml

    # /blog/2009/sept/18/are-my-services-coool.yml
    type: presentation.reveal
    title: How to create a good presentation ?
    published_at: 20 May 2014 12:37:48

    ----
    ## The presentation
    ----
    ## Slide 1

    - My bullet point 1
    - My bullet point 2

    ----
    data-state: blackout

    ## Slide 2

    - My bullet point 1
    - My bullet point 2

    ----
    ### etc ..

    ...

You can use some metadata to get better support from the theme

- ``data-state`: used to change the background color

Slideshare Presentation
-----------------------

A shower presentation is defined by ``presentation.slideshare`` node type:

.. code-block:: yaml

    type: presentation.slideshare
    title: SFPot March 2014 - Sonata Block Bundle
    published_at: 19 March 2014 12:37:48
    embed_code: 32480268 # the embed code
    width: 800           # the width of the presentation (default=597)