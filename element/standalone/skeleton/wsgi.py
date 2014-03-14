# -*- coding: UTF-8 -*-
"""
This script must by the wsgi handler to start the application. 

You can customize it for your need.
"""
import os, logging, sys, tornado
from start import get_container


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

if __name__ == '__main__':
    application = get_container(parameters).get("ioc.extra.tornado.application")
    application.listen(8888)

    tornado.ioloop.IOLoop.instance().start()