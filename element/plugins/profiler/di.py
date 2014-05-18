import ioc
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/profiler.yml" % path, container_builder)

        container_builder.parameters.set('element.plugins.profiler.output_dir', config.get_all('output_dir', '%project.root_folder%/data/profiler'))
