Page
====

Features
--------

  - Expose a ``page.default`` node handler


Configuration
-------------

There is no configuration option. You only need to enable the plugin by adding this line into the IoC configuration file.

.. code-block:: yaml

    element.plugins.page:

Usage
-----

A page node is very similar to a blog node, however it should be used to render simple page.

.. code-block:: yaml

title: Homepage
type: page.default
format: html
content: |

    <div class="row demo-tiles">
        <div class="span3">
          <div class="tile">
            <img class="tile-image big-illustration" alt="" src="images/illustrations/colors.png" />
            <h3 class="tile-title">Blog</h3>
            <p>Some posts about <br/>technicals playground.</p>
            <a class="btn btn-primary btn-large btn-block" href="blog">Read It</a>
          </div>
        </div>

        <div class="span3">
          <div class="tile">
            <img class="tile-image" alt="" src="images/illustrations/infinity.png" />
            <h3 class="tile-title">Element</h3>
            <p>A python CMS based on flask with a bit of IOC. </p>
            <a class="btn btn-primary btn-large btn-block" href="https://github.com/rande/python-element">Play</a>
          </div>
        </div>

        <div class="span3">
          <div class="tile">
            <img class="tile-image" alt="" src="images/illustrations/bag.png" />
            <h3 class="tile-title">Stats</h3>
            <p>Some information about this instance.</p>
            <a class="btn btn-primary btn-large btn-block" href="stats/parameters">Get Them</a>
          </div>
        </div>

        <div class="span3">
          <div class="tile">
            <img class="tile-image" alt="" src="images/illustrations/compass.png" />
            <h3 class="tile-title">Resume</h3>
            <p>A "standard" <br />curriculum vitae.</p>
            <a class="btn btn-primary btn-large btn-block" href="resume">Discover It</a>
          </div>

        </div>
      </div>

The ``format`` option defines how to handle the ``content`` field. You can provide a markdown content or a html content.
