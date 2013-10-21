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

    git clone https://github.com/rande/python-simple-ioc.git
    pip install --requirements_test.txt

Checking installation
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    unit2 discover

Running dummy site
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    python element/standalone/skeleton/loads.py # load some data into mongodb
    python element/standalone/skeleton/wsgi.py  # start the wsgi application