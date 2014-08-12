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

# References used to code this file
#   - https://raw.githubusercontent.com/tornadoweb/tornado/master/tornado/autoreload.py

import os
import sys
import types
import fnmatch
import logging
import socket, re

import tornado.httpclient
from tornado.iostream import IOStream
from tornado.tcpserver import TCPServer
from tornado.httputil import HTTPHeaders

gen_log = logging.getLogger("tornado.general")

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

class FilesWatcher(object):
    def __init__(self, paths=None):
        self._watched_files = set()
        self._reload_hooks = []
        self._reload_attempted = False
        self.delay = 0

        self.paths = paths or []
        self.patterns = ["*.py", "*.html"]

    def start(self, io_loop=None, check_time=2000):

        self.build_watched_files()

        self.io_loop = io_loop or tornado.ioloop.IOLoop.current()

        self.modify_times = {}

        gen_log.info("%d files to watch" % len(self._watched_files))

        # tornado.ioloop.PeriodicCallback(self.build_watched_files, 5000, io_loop=self.io_loop).start()
        tornado.ioloop.PeriodicCallback(self._reload_on_update, check_time, io_loop=self.io_loop).start()

    def build_watched_files(self):
        gen_log.info("Reloading watched files")
        self._watched_files = set()
        for path in self.paths:
            for pattern in self.patterns:
                for file in find_files(path, pattern):
                    self.watch(file)

    def watch(self, filename):
        self._watched_files.add(filename)

    def add_reload_hook(self, fn):
        self._reload_hooks.append(fn)

    def _reload_on_update(self):
        self.delay += 1

        for module in sys.modules.values():
            # Some modules play games with sys.modules (e.g. email/__init__.py
            # in the standard library), and occasionally this can cause strange
            # failures in getattr.  Just ignore anything that's not an ordinary
            # module.
            if not isinstance(module, types.ModuleType):
                continue

            path = getattr(module, "__file__", None)

            if not path:
                continue

            if path.endswith(".pyc") or path.endswith(".pyo"):
                path = path[:-1]

            self._check_file(path)

        for path in self._watched_files:
            if self._check_file(path):
                self.delay = 0
                self._reload(path)

                return

    def _check_file(self, path):
        try:
            stat = os.stat(path)
            modified = "%s-%s" % (stat.st_mtime, stat.st_size)
        except Exception:
            return

        if path not in self.modify_times:
            self.modify_times[path] = modified
            return False

        if self.modify_times[path] != modified:
            self.modify_times[path] = modified
            return True

        return False

    def _reload(self, path):
        self.delay = 0

        for fn in self._reload_hooks:
            self.io_loop.add_callback(fn, path)

class ProxyState(object):
    def __init__(self, command):
        self.reloading = False
        self.command = command
        self.process = False

    def start(self):
        gen_log.info("Start command: %s " % self.command)
        self.process = tornado.process.Subprocess(self.command, shell=False)
        self.process.set_exit_callback(self._restart)

    def _restart(self, code):
        if self.reloading:
            gen_log.info("Create a new process !!")
            self.start()
            self.reloading = False

    def restart(self, *args, **kwargs):
        self.reloading = True

        if not self.process.proc.returncode:
            gen_log.info("Terminate process")
            self.process.proc.kill()

def parse_headers(data):
    headers = HTTPHeaders()

    for line in data.splitlines():
        if line:
            try:
                headers.parse_line(line)
            except Exception, e:
                break

    return headers

def is_websocket(headers):
    """
    Detect if the data is related to a websocket connection, should be called only once

    http://en.wikipedia.org/wiki/WebSocket
    """
    return "Upgrade" in headers and headers["Upgrade"] == "websocket"

class StreamProxy(object):
    def __init__(self, io_source, io_target):
        self.public_io = io_source
        self.internal_io = io_target

        self.reset()

    def reset(self):
        self.init = False
        self.is_websocket = None
        self.is_html = None

        self.public_headers = None
        self.internal_headers = None

        self.content_length = 0

    def handle(self):
        self.public_io.read_until_close(callback=self.end_public, streaming_callback=self.proxy_data_to_internal)
        self.internal_io.read_until_close(callback=self.end_internal, streaming_callback=self.proxy_data_to_public)

    def end_public(self, data):
        gen_log.debug("Proxy   > callback end_public")
        self.internal_io.close()

    def end_internal(self, data):
        gen_log.debug("Proxy   > callback end_internal")
        self.public_io.close()

    def proxy_data_to_internal(self, data):
        """
        This method is used to send streamed data to the internal webserver
        """
        if not self.init:
            self.init = True

            request, headers = data.split("\r\n", 1)
            gen_log.info("request: %s" % request)

            self.public_headers = parse_headers(headers)
            self.is_websocket = is_websocket(self.public_headers)

            if not self.is_websocket:
                # we don't want to deal with gzip content
                data = data.replace("Accept-Encoding: gzip, deflate\r\n", "")

        self.internal_io.write(data)

    def close_stream(self):
        if self.internal_headers and 'Content-Length' in self.internal_headers and self.content_length >= int(self.internal_headers['Content-Length']):
            if self.public_io.writing():
                gen_log.debug("  > still data being written")

                return

            gen_log.debug("  > closing all streams")

            self.public_io.close()
            self.internal_io.close()

            self.reset()

    def proxy_data_to_public(self, data):
        if self.is_websocket:
            self.public_io.write(data)
            return

        if not self.internal_headers:
            # we parse the response to replace esi tag
            self.internal_headers = parse_headers(data.split("\r\n", 1)[1])

            self.is_html = 'Content-Type' in self.internal_headers and self.internal_headers['Content-Type'].startswith('text/html')

        self.content_length += len(data)

        if self.is_html and 'Content-Length' in self.internal_headers:
            data = data.replace('Content-Length:', 'X-Content-Length:')
            data = self.replace_tag(data)

        self.public_io.write(data, callback=self.close_stream)

    def replace_tag(self, data):
        client = tornado.httpclient.HTTPClient()
        headers = self.public_headers.copy()
        headers['Surrogate-Capability'] = 'abc=ESI/1.0'

        if 'Set-Cookie' in self.internal_headers:
            headers['Cookie'] = self.internal_headers['Set-Cookie']

        if 'Accept-Encoding' in headers:
            # we don't want to deal with gzip content
            del(headers['Accept-Encoding'])

        def get_contents(matcher):
            result = urlparse(matcher.group(2))

            url = "http://%s%s?%s" % ("localhost:5001", result.path, result.query)

            try:
                gen_log.info("  > start sub-request: %s" % url)

                sub_response = client.fetch(tornado.httpclient.HTTPRequest(url, headers=headers))

                gen_log.debug("  > end sub-request: %s" % url)

                return sub_response.body
            except tornado.httpclient.HTTPError as e:
                return "<!-- error resolving : %s !-->" % url

        content = re.sub(r"<esi:include\W[^>]*src=(\"|')([^\"']*)(\"|')[^>]*/>", get_contents, data, flags=re.IGNORECASE)

        return content

class ProxyTCPServer(TCPServer):
    def __init__(self, sub_child_port, **kwargs):
        self.sub_child_port = sub_child_port

        super(ProxyTCPServer, self).__init__(**kwargs)

    def handle_stream(self, io_source, address):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        io_target = IOStream(s)

        proxy = StreamProxy(io_source, io_target)
        io_target.connect(("localhost", self.sub_child_port), proxy.handle)
