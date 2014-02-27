Blog
====

Features
~~~~~~~~

  - Expose a ``blog.post`` node handler


Configuration
-------------

There is no configuration option. You only need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.blog:

Usage
-----

You can create a blog index by creating a ``node.index`` node  with the following value. The node will list all children of ``/blog`` with types = ``blog.post``.

.. code-block:: yaml

    # /blog/_index.yml
    title: Posts
    type: node.index
    filters:
        limit: 64
        path: /blog
        types: [blog.post]


A blog post is defined as:

.. code-block:: yaml

    # /blog/2009/sept/18/are-my-services-coool.yml
    type: blog.post
    title: Are my services coool ?
    format: markdown
    enabled: 1
    published_at: Fri, 18 Sep 2009 19:19:16
    comment_enabled:
    content: |
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras gravida malesuada tellus,
        at tincidunt lorem accumsan vel. Vestibulum varius sodales sagittis. Quisque tristique
        tempus ligula blandit sodales. Nunc luctus, orci in interdum porttitor, urna massa scelerisque
        felis, eget hendrerit sapien eros sed augue. Ut quam mauris, feugiat nec laoreet pellentesque,
        molestie eget orci. Vivamus leo leo, convallis et sodales vel, fermentum sed leo. Cras sit
        amet dui vel sapien consectetur adipiscing. Pellentesque lectus massa, aliquet et ultrices
        sit amet, volutpat vel leo. Nulla aliquet sodales enim ac dictum. Proin mattis arcu a metus
        aliquam pulvinar. Phasellus sed lectus elit. Donec vitae urna magna. Vestibulum id volutpat eros.

The ``format`` option defines how to handle the ``content`` field. You can provide a markdown content or a html content.

Events
------

The default template used is ``element.plugins.blog:post.html`` and declare two nodes events that can be used to extends the template.

- ``node.comment.list``: the listener should return the comment list related to the provided node
- ``node.comment.form``: the listener should return the comment form

The :doc:`element.plugins.discus</plugins/discus>` plugin can be used to handle comments.
