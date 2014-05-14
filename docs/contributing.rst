Contributing
============

Thanks for going into this section! This page tries to summaries all information required to contribute to this project.
Any contribution must have its own unit tests to ensure good quality and avoid regressions.


Retrieving the code
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    git clone https://github.com/rande/python-element.git
    pip install -e python-element
    cd python-element

Loading fixtures
~~~~~~~~~~~~~~~~

The repository comes with a set of fixtures that you can load to test the solution, or improve it! To load them just
run the following commands::

    make fixtures

Unit Tests
~~~~~~~~~~

Unit tests are important to avoid bugs. The current test suite used nosetests, to run tests::

    make test

Running code
~~~~~~~~~~~~

Once fixtures are loaded, you can start the http webserver with the command::

    make dev

Documentations
~~~~~~~~~~~~~~

English is not the first language of programmers, some typos or huge grammatical errors might occur in this project,
please feel free to fix them by sending some pull requests.

Of course you are welcome to contributing to the documentation too!