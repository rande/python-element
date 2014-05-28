Presentation
============

Features
--------

  - Expose a ``presentation.shower`` node handler to render a node with the shower presentation tools


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

