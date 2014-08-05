# -*- coding: utf-8 -*-

# This script initialize a small reverse proxy with a basic support for
# rendering esi:include tag.

import sys, os, tornado
from element.proxy import ProxyState, FilesWatcher, ProxyTCPServer
import logging

logging.basicConfig(format="[%(asctime)-15s] proxy.%(levelname)s: %(message)s")

gen_log = logging.getLogger("tornado.general")
gen_log.setLevel(logging.INFO)

if __name__ == '__main__':
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    sub_child_port = 5001
    if len(sys.argv) > 2:
        sub_child_port = int(sys.argv[2])

    child_process = [
        '%s' % (sys.executable), 'start.py', 'tornado:start',
        # Debug parameters
        '--verbose', '-d',
        # Start only one child, otherwise the Suprocess module will not be able to
        # properly kill sub children process
        # There is no need to have more than once ...
        '-np', '1',
        # The subprocess will listen to port 5001, and the master to 5001
        '-p', str(sub_child_port),
        # The bind parameter is used to define the host used to render absolute urls
        '--bind', 'element.vagrant:%d' % port
    ]

    print("Starting HTTP proxy on port %d" % port)
    print(" > %s" % " ".join(child_process))

    state = ProxyState(child_process)

    server = ProxyTCPServer(sub_child_port)
    server.bind(port)
    server.start(1)  # Forks multiple sub-processes

    if tornado.process.task_id() == 0 or not tornado.process.task_id():
        w = FilesWatcher([
            os.path.dirname(os.path.abspath(__file__)),
            # '/home/vagrant/python/element'
            # add more path to watch
        ])

        w.add_reload_hook(state.restart)
        w.start()
        state.start()

    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()