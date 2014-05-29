Node
====

It is the smallest data available, it represents a content stored into the datastore. By default, a node is a instance of ``Node``.

NodeContext
~~~~~~~~~~~

The ``NodeHandler`` is in charge of rendering a ``Node`` by using an intermediary object the ``NodeContext``. The ``NodeContext`` hold altered the information from the ``Node``, a ``NodeContext`` should never be persisted while the ``Node`` can. The ``Node`` is still available from the ``NodeContext`` by using the ``node`` attribute.

Change the default Node class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to change the default class ``Node`` per node type. (The underlying mechanism change the ``__class__`` property).

In order to do that, you need to create a specific listener to register the ``class`` with the ``type``

.. code-block:: yaml

    element.plugins.presentation.listener:
        class: element.plugins.presentation.listener.PresentationListener
        tags:
            event.listener:
                - { name: node.mapper.pre_initialize, method: register }

The related python is:

.. code-block:: python

    class PresentationListener(object):
        def register(self, event):
            collection = event.get('meta_collection')

            collection.add(Meta(PresentationNode, 'presentation.shower'))


Inside the ``PresentationNode``, you can have your own logic and methods

.. code-block:: python

    class PresentationNode(Node):
        def __init__(self, uuid=None, data=None):
            super(PresentationNode, self).__init__(uuid=uuid, data=data)

        def count_slides():
            return len(self.data['slides'])