Install
=======

Python Element has been tested with python 2.7 only and might not work with python 3.x.

Short story
~~~~~~~~~~~

.. code-block:: bash

    sudo apt-get install mongodb-server
    virtualenv --system-site-packages foobar
    source foobar/bin/activate
    pip install git+http://github.com/rande/python-element.git
    python -m element my-project
    cd my-project
    python start.py element:demo:fixtures
    python start.py tornado:start --verbose -d


Install services
~~~~~~~~~~~~~~~~

The default skeleton required a mongodb server running, this is not mandatory for small website.

.. code-block:: bash

    apt-get install mongodb-server

Install with virtual env
~~~~~~~~~~~~~~~~~~~~~~~~

Virtual Env makes sure there are not conflict with any installed lib by creating its own environment.

.. code-block:: bash

    virtualenv --system-site-packages element
    source element/bin/activate

Install python element
~~~~~~~~~~~~~~~~~~~~~~

You can install the package by using the main code on github

.. code-block:: bash

    pip install git+http://github.com/rande/python-element.git

Setup your first project
~~~~~~~~~~~~~~~~~~~~~~~~

The following command will help you creating your first project based on a skeleton website that you can tweak to
match your needs.

.. code-block:: bash

    python -m element my-project

The script will explain the next steps.