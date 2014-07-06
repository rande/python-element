
# References used to code this file
#   - https://github.com/senko/tornado-proxy/blob/master/tornado_proxy/proxy.py
#   - https://raw.githubusercontent.com/tornadoweb/tornado/master/tornado/autoreload.py

import socket
import tornado.httpserver
import tornado.web
import tornado.httpclient
import os
import sys
import types
import fnmatch
import re

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

        print("%d files to watch" % len(self._watched_files))
        # tornado.ioloop.PeriodicCallback(self.build_watched_files, 5000, io_loop=self.io_loop).start()
        tornado.ioloop.PeriodicCallback(self._reload_on_update, check_time, io_loop=self.io_loop).start()

    def build_watched_files(self):

        print("Reloading watched files")
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
        self.process = tornado.process.Subprocess(self.command, shell=False)
        self.process.set_exit_callback(self._restart)

    def _restart(self, code):
        if self.reloading:
            print("Create a new process")
            self.start()
            self.reloading = False

    def restart(self, *args, **kwargs):
        self.reloading = True
        if self.process.proc.returncode != None:
            self.process.proc.terminate()

class ProxyHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ['GET', 'POST', 'CONNECT']

    def initialize(self, state, proxy=None):
        self.state = state
        self.client = tornado.httpclient.AsyncHTTPClient()
        self.proxy = proxy or 'localhost:5001'

    def handle_response(self, response):
        if response.error and not isinstance(response.error, tornado.httpclient.HTTPError):
            self.set_status(500)
            self.write('Internal server error:\n' + str(response.error))
        else:
            self.set_status(response.code)

            for header in ('Date', 'Cache-Control', 'Server', 'Content-Type', 'Location'):
                v = response.headers.get(header)

                if v:
                    self.set_header(header, v)

            if not response.body:
                return

            if response.headers['Content-Type'].startswith('text/html'):
                self.write(self.replace_tag(response))
            else:
                self.write(response.body)

        self.finish()

    def replace_tag(self, response):
        client = tornado.httpclient.HTTPClient()
        headers = self.request.headers.copy()
        headers['Surrogate-Capability'] = 'abc=ESI/1.0'

        if 'Set-Cookie' in response.headers:
            headers['Cookie'] = response.headers['Set-Cookie']

        def get_contents(matcher):
            result = urlparse(matcher.group(2))

            url = "http://%s%s?%s" % (self.proxy, result.path, result.query)

            try:
                print("FETCHING ESI TAG: %s" % url)

                sub_response = client.fetch(tornado.httpclient.HTTPRequest(url, headers=headers))

                return sub_response.body
            except tornado.httpclient.HTTPError as e:
                return "<!-- error resolving : %s !-->" % url

        content = re.sub(r"<esi:include\W[^>]*src=(\"|')([^\"']*)(\"|')[^>]*/>", get_contents, response.body, flags=re.IGNORECASE)

        return content

    @tornado.web.asynchronous
    def get(self):

        if self.state.reloading:
            self.write("reloading")

            self.finish()
            return

        url = "%s://%s%s" % ('http', self.proxy, self.request.uri)

        print("PROXY: Task: %s - %s %s" % (tornado.process.task_id(), self.request.method, url))

        req = tornado.httpclient.HTTPRequest(url=url,
            method=self.request.method, body=self.request.body,
            headers=self.request.headers, follow_redirects=False,
            allow_nonstandard_methods=True
        )

        try:
            self.client.fetch(req, self.handle_response)
        except tornado.httpclient.HTTPError as e:
            if hasattr(e, 'response') and e.response:
                self.handle_response(e.response)
            else:
                self.set_status(500)
                self.write('Internal server error:\n' + str(e))
                self.finish()

    @tornado.web.asynchronous
    def post(self):
        return self.get()

    @tornado.web.asynchronous
    def connect(self):
        host, port = self.request.uri.split(':')
        client = self.request.connection.stream

        def read_from_client(data):
            upstream.write(data)

        def read_from_upstream(data):
            client.write(data)

        def client_close(data=None):
            if upstream.closed():
                return
            if data:
                upstream.write(data)
            upstream.close()

        def upstream_close(data=None):
            if client.closed():
                return
            if data:
                client.write(data)
            client.close()

        def start_tunnel():
            client.read_until_close(client_close, read_from_client)
            upstream.read_until_close(upstream_close, read_from_upstream)
            client.write(b'HTTP/1.0 200 Connection established\r\n\r\n')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        upstream = tornado.iostream.IOStream(s)
        upstream.connect((host, int(port)), start_tunnel)
