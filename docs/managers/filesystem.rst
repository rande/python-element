Filesystem
==========

Features
~~~~~~~~

  - Load contents from a yaml file

Configuration
~~~~~~~~~~~~~

There is no configuration option.


Usage
~~~~~

You can create a yaml file with the following structure:

.. code-block:: yaml

    title: Inline Content
    type: blog.post
    tags: ['red', 'yellow']

    ----
    ## my title
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean rutrum diam
    lectus, eget ultricies purus. Suspendisse pellentesque enim ullamcorper libero
    adipiscing vulputate.

    ## section 1
    Curabitur velit ipsum, sagittis volutpat porta at, imperdiet at risus. Donec ipsum nunc,
    commodo ut laoreet sed, mollis eu dolor. Praesent iaculis, nisl a laoreet elementum,
    odio lacus aliquam risus, et aliquam turpis metus vestibulum dolor.

    Maecenas venenatis nulla in metus egestas sollicitudin. Donec convallis sodales
    massa, ac feugiat mauris tincidunt vel. Fusce eu leo vel nisi faucibus luctus.


.. note::

    As you notice the file is not a valid yaml file, all the data after the ``----`` separator will be available in the ``content`` field of the node object