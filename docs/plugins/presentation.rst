Presentation
============

Features
--------

  - Expose a ``presentation.shower`` node handler to render a node with the `shower presentation tools <https://github.com/shower/shower>`_


Configuration
-------------

There is no configuration option. You only need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.presentation:


Bower configuration
~~~~~~~~~~~~~~~~~~~

You need to install ``shower``, open your bower.json file and add

.. code-block:: json

    "dependencies": {
        "shower": "~1"
    }

Usage
-----

A presentation is defined as:

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

Advance Usage
-------------

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
