Events
~~~~~~

element.request
---------------

This event is used when a request is received by Flask. Events registered:

* ``element.plugins.security.firewall`` : this is the security firewall used to control resource access depends on user's
    credentials and depends role required to access to the resource.

element.response
----------------

* ``element.plugins.security.handler.FlaskContextHandler``: this is used to store security information into the user's session

element.nodes.load.success
--------------------------

This event is used when a set of nodes is loaded. While a node is loaded, no ``element.node.load.success`` event is notified.

element.node.load.success
-------------------------

This event is used when a node is loaded.

element.node.load.fail
----------------------

This event is used when a node cannot be found

element.node.pre_delete
-----------------------

This event is used when a node will be deleted.

element.node.post_delete
------------------------

This event is used when a node has been deleted.

element.node.pre_save
---------------------

This event is used when a node will be saved.

element.node.post_save
----------------------

This event is used when a node has been saved.
