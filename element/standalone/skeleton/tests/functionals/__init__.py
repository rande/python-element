# vim: set fileencoding=utf-8 :

import sys, os, json
from tornado.testing import AsyncHTTPTestCase

base = sys.path[0]
sys.path.insert(0, base + "/../../../")
sys.path.insert(0, base + "/../../../../../")

from start import get_container

import element
from element.manager import get_uuid

parameters = {
    'ioc.debug': True,
    'ioc.env': 'prod',
    'project.root_folder': os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../..')
}

application = get_container(parameters).get("ioc.extra.tornado.application")

class AuthAsyncHTTPTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return application

    def do_fetch(self, url, **kwargs):
        kwargs['auth_username'] = 'admin'
        kwargs['auth_password'] = 'admin'

        return self.fetch(url, **kwargs)

    def get(self, url, **kwargs):
        return self.do_fetch(url, **kwargs)

    def delete(self, url, **kwargs):
        return self.do_fetch(url, method="DELETE", **kwargs)

    def put_json(self, url, data, **kwargs):
        kwargs['headers'] = {'Content-Type': 'application/json'}

        response = self.do_fetch(url, method="PUT", body=json.dumps(data), **kwargs)

        return response, json.loads(response.body)

    def post_json(self, url, data, **kwargs):
        kwargs['headers'] = {'Content-Type': 'application/json'}

        response = self.do_fetch(url, method="POST", body=json.dumps(data), **kwargs)

        return response, json.loads(response.body)

    def delete_json(self, url, **kwargs):
        kwargs['headers'] = {'Content-Type': 'application/json'}

        response = self.do_fetch(url, method="DELETE", **kwargs)

        return response, json.loads(response.body)
