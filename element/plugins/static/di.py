import ioc
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/handler_static.yml" % path, container_builder)

        container_builder.parameters.set('element.static.mapping', {
            'jpg': 'image/jpeg',
            'JPG': 'image/jpeg',
            'png': 'image/png',
            'PNG': 'image/png',
            'gif': 'image/gif',
            'GIF': 'image/gif',
            'js': 'application/x-javascript; charset=utf-8',
            'css': 'text/css; charset=utf-8',
            'json': 'application/json; charset=utf-8',
            'txt': 'text/plain; charset=utf-8',
            'xml': 'text/xml; charset=utf-8',
            'rss': 'application/rss+xml; charset=utf-8',
            'ico': 'image/x-icon'
        })

    def post_build(self, container_builder, container):

        router = container.get('ioc.extra.tornado.router')

        router.add('element.static', '/element/static/<string:module>/<path:filename>', **{
            'methods': ['GET'],
            'view_func': container.get('element.plugins.static.view').execute
        })
