import ioc
from ioc.component import Definition, Reference
import os, re

from .auth.basic import HttpBasicSecurityFactory

class Extension(ioc.component.Extension):

    listenerPositions = ['pre_auth', 'form', 'http', 'remember_me']

    def __init__(self):
        self.factories = {}
        for position in self.listenerPositions:
            self.factories[position] = []

        self.add_factory(HttpBasicSecurityFactory())

    def add_factory(self, factory):
        self.factories[factory.position].append(factory)

    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/security.yml" % path, container_builder)
        loader.load("%s/resources/config/auth.yml" % path, container_builder)

        self.configure_role_hierarchie(config.get_dict('role_hierarchy', {}), container_builder)
        self.configure_providers(config.get_dict('providers'), container_builder)
        self.configure_access_map(config.get('access_control', []), container_builder)
        self.configure_firewalls(config.get_dict('firewalls', {}), container_builder)

    def configure_role_hierarchie(self, config, container_builder):
        container_builder.get('element.plugins.security.role.hierarchy').arguments[0] = config.all()

    def configure_providers(self, config, container_builder):
        self.configure_inmemory_provider(config.get_dict('in_memory'), container_builder)

    def configure_inmemory_provider(self, config, container_builder):
        container_builder.parameters.set('element.plugins.security.in_memory_users', config.get('users', []))

    def configure_access_map(self, map, container_builder):
        definition = container_builder.get('element.plugins.security.access_map')

        for value in map:
            definition.add_call('add', arguments=[re.compile(value['path']), value['role']])

    def configure_firewalls(self, config, container_builder):
        auth_providers = []

        parameter = []
        for name, settings in config.all().iteritems():
            pattern = settings.get('pattern', '.*')

            parameter.append((re.compile(pattern), self.get_firewall_context(name, settings, container_builder, auth_providers)))
            
        container_builder.get('element.plugins.security.firewall_map').arguments = [parameter]

        container_builder.get('element.plugins.security.auth.manager').arguments[1] = [Reference(provider) for provider in auth_providers]


    def get_firewall_context(self, name, settings, container_builder, auth_providers):
        handlers = []

        # create the FlaskContextHandler, this service load token from flask session handling
        context_handler = Definition('element.plugins.security.handler.TornadoContextHandler', [
            Reference('element.plugins.security.context'),
            Reference('element.plugins.security.provider.in_memory'), # this need to be configurable
            settings.get('context', name)
        ], {'logger': Reference('element.logger')})

        context_handler.add_tag('event.listener', { 
            'name': 'handler.response',
            'method': 'handleResponse', 
            'priority': 32 
        })

        handlers.append(context_handler)

        for position in self.listenerPositions:
            for factory in self.factories[position]:
                if not settings.get(factory.key):
                    continue

                auth_provider_id, handler_id, entry_point_id = factory.create(container_builder, name, settings.get(factory.key))

                handlers.append(Reference(handler_id))
                auth_providers.append(auth_provider_id)

        container_builder.add('element.plugins.security.handlers.tornado_context.%s' % name, context_handler)

        if settings.get("anonymous", False):
            id_anonymous = 'element.plugins.security.listener.anonymous.%s' % name
            container_builder.add(id_anonymous, Definition('element.plugins.security.handler.AnonymousAuthenticationHandler', 
                [name, Reference('element.plugins.security.context')],
                {'logger': Reference('element.logger')}
            ))

            handlers.append(Reference(id_anonymous))

        handlers.append(Reference('element.plugins.security.handlers.access_map'))

        return (handlers, None)

