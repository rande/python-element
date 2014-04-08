# vim: set fileencoding=utf-8 :

import sys, os, json, ioc, logging
from tornado.testing import AsyncHTTPTestCase

base = sys.path[0]
sys.path.insert(0, base + "/../../../")
sys.path.insert(0, base + "/../../../../../")


import element
from element.manager import get_uuid

parameters = {
    'ioc.debug': True,
    'ioc.env':   'test',
    'project.root_folder': os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../..')
}

files = [
    '%s/config/config.yml' % (parameters['project.root_folder']),
    '%s/config/services.yml' % (parameters['project.root_folder']),
    '%s/config/parameters_%s.yml' % (parameters['project.root_folder'], parameters['ioc.env']),
]

container = ioc.build(files, logger=logging.getLogger('test'), parameters=parameters)

application = container.get("ioc.extra.tornado.application")

# dispatch the tornado events ..
container.get('ioc.extra.event_dispatcher').dispatch('ioc.extra.tornado.start', {
    'application': application
})

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
