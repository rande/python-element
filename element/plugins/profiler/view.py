__author__ = 'rande'


class ProfilerView(object):
    def __init__(self, profiler):
        self.profiler = profiler


    def home(self):
        pass

    def view(self, request_handler, token, **kwargs):

        panel = request_handler.get_argument('panel')

        run = self.profiler.load_run(token)

        return 200, self.profiler.get_template_name(run, panel), {
            'run': run,
            'panel': panel,
            'collector': run.get_metric(panel),
            'templates': self.profiler.get_templates(run),
            'token': token,
            'position': 'bottom',
            'profile': run,
            'is_ajax': request_handler.is_xml_http_request()
        }

    def pyinfo(self, request_handler, token, **kwargs):
        pass

    def wdt(self, request_handler, token, **kwargs):

        run = self.profiler.load_run(token)

        return 200, 'element.plugins.profiler:profiler/toolbar.html', {
            'run': run,
            'token': token,
            'position': 'bottom',
            'profile': run,
            'templates': self.profiler.get_templates(run)
        }

    def export_run(self):
        pass

    def purge_run(self):
        pass

    def import_run(self):
        pass
