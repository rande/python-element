Disqus
======

Features
--------

  - Add a custom block to include disqus comments

Configuration
-------------

You need to enabled the ``element.plugins.disqus`` module.

.. code-block:: yaml

    element.plugins.disqus:
        account: account_code


The ``account`` value is the name of your account on disqus.

Events
------

 - The plugin uses the ``node.comment.list`` event to add the comment list.
