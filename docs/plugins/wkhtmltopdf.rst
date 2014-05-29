Wkhtmltopdf
===========

Features
--------

  - Add a form to generate a PDF from a provided url using wkhtmltopdf (the software must be available in your path)

Configuration
-------------

There is no configuration option. You only need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.wkhtmltopdf:
        # where the generated pdf will be stored
        data_path: %project.root_folder%/data/wkhtmltopdf

Usage
-----

Just place a store a file in the datasource and access it with a browser. That's it.

.. code-block::

    # pdf.yml
    title: PDF generation
    type: action.raw
    name: wkhtmltopdf_index
    methods: ['GET']
    defaults:
        _controller: element.plugins.wkhtmltopdf.generate:execute
