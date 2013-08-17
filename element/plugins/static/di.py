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

    def post_load(self, container_builder):
        definition = container_builder.get('element.flask.blueprint')

        definition.add_call(
            'add_url_rule', 
            ['element/static/<string:module>/<path:path>'],
            {
                'methods': ['GET'], 
                'view_func': ioc.component.Reference('element.flask.plugins.static.view')
            }
        )
