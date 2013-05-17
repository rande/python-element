import ioc
import os
import re

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/services.yml" % path, container_builder)
        loader.load("%s/resources/config/jinja.yml" % path, container_builder)
        loader.load("%s/resources/config/command.yml" % path, container_builder)

        # To do: add this as a configuration option
        loader.load("%s/resources/config/handler_action.yml" % path, container_builder)
        loader.load("%s/resources/config/handler_blog.yml" % path, container_builder)
        loader.load("%s/resources/config/handler_disqus.yml" % path, container_builder)
        loader.load("%s/resources/config/handler_contact.yml" % path, container_builder)
        loader.load("%s/resources/config/handler_seo.yml" % path, container_builder)
        loader.load("%s/resources/config/handler_page.yml" % path, container_builder)
        loader.load("%s/resources/config/handler_static.yml" % path, container_builder)
        loader.load("%s/resources/config/handler_redirect.yml" % path, container_builder)

        # To do: add this as a configuration option
        loader.load("%s/resources/config/listener_standardize.yml" % path, container_builder)
        loader.load("%s/resources/config/listener_seo.yml" % path, container_builder)
        loader.load("%s/resources/config/listener_default_index.yml" % path, container_builder)
        loader.load("%s/resources/config/listener_errors.yml" % path, container_builder)
        loader.load("%s/resources/config/listener_cache.yml" % path, container_builder)
        loader.load("%s/resources/config/listener_actions.yml" % path, container_builder)

        container_builder.parameters.set('element.web.public.dir', config.get('public_dir', "%s/resources/public" % path))
        container_builder.parameters.set('element.template.dir', config.get('template', "%s/resources/template" % path))
        container_builder.parameters.set('element.static.dir', config.get('static', "%s/resources/static" % path))
        container_builder.parameters.set('element.web.base_url', config.get('base_url', "/node"))
        container_builder.parameters.set('element.static.mapping', {
            'jpg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'js': 'application/x-javascript; charset=utf-8',
            'css': 'text/css',
            'json': 'application/json',
        })

        if not config.get('data_dir', False):
            raise Exception("Please configure the data_dir settings")

        container_builder.parameters.set('element.data.dir', config.get('data_dir', False))

        self.configure_flask(config, container_builder)
        self.configure_handlers(config, container_builder)
        self.configure_seo(config, container_builder)
        self.configure_cache(config, container_builder)

    def configure_flask(self, config, container_builder):
        definition = container_builder.get('element.flask.blueprint')

        definition.add_call(
            'add_url_rule', 
            ['/'],
            {'methods': ['POST', 'GET'], 'view_func': ioc.component.Reference('element.flask.view.index'), 'defaults': {'path': '/'}}
        )

        definition.add_call(
            'add_url_rule', 
            ['/<path:path>'],
            {'methods': ['POST', 'GET'], 'view_func': ioc.component.Reference('element.flask.view.index')}
        )

    def configure_seo(self, config, container_builder):
        seo = config.get('seo', {
            'title_pattern': 'Python Element : %s'
        })
        
        container_builder.parameters.set('element.seo.page.title_pattern', seo.get('title_pattern'))

    def configure_handlers(self, config, container_builder):
        handlers = config.get_dict('handlers')

        discus = handlers.get('disqus', {'account': False})

        container_builder.parameters.set('element.disqus.account', discus.get('account'))

    def configure_cache(self, config, container_builder):
        rules = []

        for rule in config.get('cache_control', {}):
            rule['path'] = re.compile(rule['path'])

            rules.append(rule)

        container_builder.parameters.set('element.cache.rules', rules)

    def post_build(self, container_builder, container):
        manager = container.get('element.node.manager')

        # register handlers
        for id in container_builder.get_ids_by_tag('element.handler'):
            definition = container_builder.get(id)
            for option in definition.get_tag('element.handler'):
                if 'name' not in option:
                    break          

                manager.add_handler(option['name'], container.get(id))

        # register loaders
        loader_chain = container.get('element.loader.chain')
        for id in container_builder.get_ids_by_tag('element.loader'):
            definition = container_builder.get(id)
            for option in definition.get_tag('element.loader'):     
                if 'name' not in option:
                    break  

                loader_chain.add_loader(option['name'], container.get(id))

