#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# This script initialize a small reverse proxy with a basic support for
# rendering esi:include tag.

import sys, os, tornado, argparse, logging
from element.proxy import ProxyState, FilesWatcher, ProxyTCPServer

logging.basicConfig(format="[%(asctime)-15s] proxy.%(levelname)s: %(message)s")

gen_log = logging.getLogger("tornado.general")
gen_log.setLevel(logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--port', '-p', help="Define the main listening port", default=5000)
    parser.add_argument('--subport', '-sp', help="Define the python element port", default=5001)
    parser.add_argument('--bind', '-b', help="Define the domain to bind to", default='localhost')

    options, argv = parser.parse_known_args(sys.argv)

    child_process = [
        '%s' % (sys.executable), 'start.py', 'tornado:start',
        # Debug parameters
        '--verbose', '-d',
        # Start only one child, otherwise the Suprocess module will not be able to
        # properly kill sub children process
        # There is no need to have more than once ...
        '-np', '1',
        # The subprocess will listen to port 5001, and the master to 5001
        '-p', str(options.subport),
        # The bind parameter is used to define the host used to render absolute urls
        '--bind', '%s:%d' % (options.bind, options.port)
    ]

    print("Starting HTTP proxy on port %d" % options.port)
    print(" > %s" % " ".join(child_process))

    state = ProxyState(child_process)

    server = ProxyTCPServer(options.subport)
    server.bind(options.port)
    # this proxy should not be used in production, so keep it simple with only one process
    server.start(1)

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