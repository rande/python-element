import ioc
from ioc.component import Definition, Reference
import os, re

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/security.yml" % path, container_builder)

        self.configure_providers(config.get_dict('providers'), container_builder)
        self.configure_access_map(config.get('access_control', []), container_builder)
        self.configure_firewalls(config.get_dict('firewalls', {}), container_builder)

    def configure_providers(self, config, container_builder):
        self.configure_inmemory_provider(config.get_dict('in_memory'), container_builder)

    def configure_inmemory_provider(self, config, container_builder):
        container_builder.parameters.set('element.plugins.security.in_memory_users', config.get('users', []))

    def configure_access_map(self, map, container_builder):
        definition = container_builder.get('element.plugins.security.access_map')

        for value in map:
            definition.add_call('add', arguments=[re.compile(value['path']), value['role']])

    def configure_firewalls(self, config, container_builder):
        self.configure_firewall_map(config, container_builder)



    def configure_firewall_map(self, config, container_builder):

        parameter = []
        for context, settings in config.all().iteritems():
            name = settings.get('context', context)
            pattern = settings.get('pattern', '.*')

            parameter.append((re.compile(pattern), self.get_firewall_context(name, settings, container_builder)))
            
        container_builder.get('element.plugins.security.firewall_map').arguments = [parameter]


    def get_firewall_context(self, name, settings, container_builder):
        handlers = []

        # create the FlaskContextHandler, this service load token from flask session handling
        context_handler = Definition('element.plugins.security.handler.FlaskContextHandler', [
            Reference('element.plugins.security.context'),
            Reference('element.plugins.security.provider.in_memory'), # this need to be configurable
            name
        ], {'logger': Reference('element.logger')})

        context_handler.add_tag('event.listener', { 
            'name': 'element.response',
            'method': 'handleResponse', 
            'priority': 32 
        })

        handlers.append(context_handler)

        container_builder.add('element.plugins.security.handlers.flask_context.%s' % name, context_handler)

        if settings.get("anonymous", False):
            id_anonymous = 'element.plugins.security.listener.anonymous.%s' % name
            container_builder.add(id_anonymous, Definition('element.plugins.security.handler.AnonymousAuthenticationHandler', 
                [name],
                {'logger': Reference('element.logger')}
            ))

            handlers.append(Reference(id_anonymous))

        handlers.append(Reference('element.plugins.security.handlers.access_map'))

        return (handlers, None)

