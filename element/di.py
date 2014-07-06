from ioc.component import Reference
import ioc
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/services.yml" % path, container_builder)
        loader.load("%s/resources/config/command.yml" % path, container_builder)

        container_builder.parameters.set('element.template.dir', config.get('template', "%s/resources/template" % path))
        container_builder.parameters.set('element.static.dir', config.get('static', "%s/resources/static" % path))
        container_builder.parameters.set('element.web.base_url', config.get('base_url', "/node"))

        self.configure_managers(config, container_builder)

    def configure_managers(self, config, container_builder):
        managers = config.get_dict('managers', {'fs': None, 'mongodb': None})

        managersList = [('fs', Reference('element.manager.fs'))]

        if not managers.get('mongodb', None):
            del container_builder.services['element.manager.mongodb']
            del container_builder.services['element.manager.mongodb.client']
            del container_builder.services['element.command.load_demo_fixtures']
        else:
            managersList.append(('mongodb', Reference('element.manager.mongodb')))

            container_builder.get('element.manager.mongodb.client').arguments[0] = config.get('mongodb.server', 'mongodb://localhost:27017/')
            container_builder.get('element.manager.mongodb').arguments[1] = config.get('mongodb.database', 'element')
            container_builder.get('element.manager.mongodb').arguments[2] = config.get('mongodb.collection.data', 'elements')

        data_dir = managers.get('fs.content', False)

        if not data_dir:
            raise Exception("Please configure the element.managers.fs.content settings")

        container_builder.parameters.set('element.data.dir', data_dir)
        container_builder.get('element.manager.fs').arguments[0] = data_dir

        container_builder.get('element.manager.chain').arguments[0] = managersList

    def post_build(self, container_builder, container):

        self.configure_tornado(container_builder, container)

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

    def configure_tornado(self, container_builder, container):
        router = container.get('ioc.extra.tornado.router')

        router.add('element.element_home', '/', **{
            'methods': ['POST', 'GET'],
            'view_func': container.get('element.tornado.view.index').execute,
            'defaults': {'path': '/'}
        })

        router.add('element.element_path', '/<path:path>', **{
            'methods': ['POST', 'GET'],
            'view_func': container.get('element.tornado.view.index').execute,
        })