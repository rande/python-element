# -*- coding: UTF-8 -*-
from start import get_container
import os, logging

"""
This script must by the wsgi handler to start the application. 

You can customize it for your need.
"""
import sys
base = sys.path[0]
sys.path.insert(0, base + "/../../../")

debug = True

if debug:
    logging.basicConfig(level=logging.DEBUG)

parameters = {
    'ioc.debug': debug,
    'ioc.env': 'prod',
    'project.root_folder': os.path.dirname(os.path.realpath(__file__))
}

app = get_container(parameters).get("ioc.extra.flask.app")

if __name__ == '__main__':
    app.run(debug=debug,host="0.0.0.0")