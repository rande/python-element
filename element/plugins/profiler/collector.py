class RequestCollector(object):

    def on_request(self, request_handler, run):
        request = request_handler.request

        request_handler.run.add_metric('request', {
            'method': request.method,
            'uri': request.uri,
            'path': request.path,
            'query': request.query,
            'version': request.version,
            'headers': request.headers,
            'protocol': request.protocol,
            'host': request.host,
            'body': request.body,
            'query_arguments': request.query_arguments,
            'body_arguments': request.body_arguments,
            'cookies': request.cookies.output(),
            'remote_ip': request.remote_ip,
        })

    def on_terminate(self, request_handler, run):
        pass