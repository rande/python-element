import ioc
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/wkhtmltopdf.yml" % path, container_builder)

        container_builder.parameters.set('element.plugins.wkhtmltopdf.data_path', config.get_all('data_path', '%project.root_folder%/data/wkhtmltopdf'))
