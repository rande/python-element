import ioc
import os
import element.event

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):

        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/services.yml" % path, container_builder)
        loader.load("%s/resources/config/handlers.yml" % path, container_builder)
        loader.load("%s/resources/config/jinja.yml" % path, container_builder)
        loader.load("%s/resources/config/disqus.yml" % path, container_builder)

        container_builder.parameters.set('element.web.public.dir', config.get('public_dir', "%s/resources/public" % path))
        container_builder.parameters.set('element.template.dir', config.get('template', "%s/resources/template" % path))
        container_builder.parameters.set('element.static.dir', config.get('static', "%s/resources/static" % path))

        if not config.get('data_dir', False):
            raise Exception("Please configure the data_dir settings")

        container_builder.parameters.set('element.data.dir', config.get('data_dir', False))

        self.configure_flask(config, container_builder)

    def configure_flask(self, config, container_builder):
        definition = container_builder.get('element.flask.blueprint')

        definition.add_call(
            'add_url_rule', 
            ['/'],
            {'view_func': ioc.component.Reference('element.flask.view.index'), 'defaults': {'path': '/'}}
        )

        definition.add_call(
            'add_url_rule', 
            ['/<path:path>'],
            {'view_func': ioc.component.Reference('element.flask.view.index')}
        )

    def post_build(self, container_builder, container):
        event_dispatcher = container.get('ioc.extra.event_dispatcher')
        # event_dispatcher.add_listener('element.node.load.fail', )
        event_dispatcher.add_listener('element.node.load.success', element.event.normalize_node)

        manager = container.get('element.node.manager')

        # register handlers
        for id in container_builder.get_ids_by_tag('element.handler'):
            definition = container_builder.get(id)
            for option in definition.get_tag('element.handler'):
                if 'name' not in option:
                    break          

                manager.add_handler(option['name'], container.get(id))

        # register loaders
        for id in container_builder.get_ids_by_tag('element.loader'):
            definition = container_builder.get(id)
            for option in definition.get_tag('element.loader'):     
                if 'name' not in option:
                    break  

                manager.add_loader(option['name'], container.get(id))
