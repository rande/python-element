Install
=======

Python Element has been tested with python 2.7 only and might not work with python 3.x.

Install services
~~~~~~~~~~~~~~~~

.. code-block:: bash

    apt-get install mongodb-server

Install with virtual env
~~~~~~~~~~~~~~~~~~~~~~~~

Virtual Env makes sure there are not conflict with any installed lib by creating its own environment.

.. code-block:: bash

    virtualenv --system-site-packages element
    source element/bin/activate

Install python element code
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install -r requirements_test.txt

Checking installation
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    make test

Running dummy site
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    make fixtures
    make dev