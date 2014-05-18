import uuid
import os

class Run(object):
    def __init__(self):
        self.data = {}
        self.metrics = {}
        self.id = uuid.uuid4()

    def add_data(self, name, value):
        self.data[name] = value

    def get_data(self, name):
        return self.data[name]

    def add_metric(self, name, value):
        self.metrics[name] = value

    def get_metric(self, name):
        return self.metrics[name]

class Profiler(object):
    def __init__(self, enabled, output_path):
        self.enabled = enabled
        self.output_path = output_path
        self.collectors = {}

    def add_collector(self, name, collector):
        self.collectors[name] = collector

    def on_request(self, event):
        request_handler = event.get('request_handler')
        request_handler.run = False

        if not self.enabled:
            return

        run = Run()

        path = "%s/%s" % (self.output_path, run.id)
        os.makedirs(path)

        request_handler = event.get('request_handler')
        request_handler.add_header('X-Profiler-Id', "%s" % run.id)
        request_handler.run = run

        for name, collector in self.collectors.iteritems():
            collector.on_request(request_handler, run)

    def on_terminate(self, event):
        request_handler = event.get('request_handler')

        if not request_handler.run:
            return

        for name, collector in self.collectors.iteritems():
            collector.on_terminate(request_handler, request_handler.run)


class RunView(object):
    def execute(self, request_handler, id, mode):
        pass