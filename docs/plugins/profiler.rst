.. note::

    This documentation is under construction, more to come soon


Profiler
========

Features
--------

  - Expose information about the current request
  - Memory Usage / Profiling ...


Configuration
-------------

There is no configuration option. You only need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.profiler:

Usage
-----

The feature is enabled on dev mode, it does not work for threaded environment.

