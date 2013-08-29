from flask.globals import request

class ElementDispatcher(object):
    def __init__(self, event_dispatcher, type, implicit_return=True, logger=None):
        self.event_dispatcher = event_dispatcher
        self.type = type
        self.implicit_return = implicit_return
        self.logger = logger

    def handle(self, subject, *args, **kwargs):
        if self.logger:
            self.logger.info("ElementDispatcher - dispatch 'element.%s' subject: %s" % (self.type, subject))

        event = self.event_dispatcher.dispatch('element.%s' % self.type, {
            self.type: subject,
            'args': args,
            'kwargs': kwargs
        })

        if self.implicit_return:
            return event.data[self.type]

class FlaskRequestElementDispatcher(ElementDispatcher):
    """
    This class is used as a proxy between Flask global request object and Element

    """
    def handle(self, *args, **kwargs):
        value = ElementDispatcher.handle(self, request, *args, **kwargs)

        return value

class FlaskResponseElementDispatcher(ElementDispatcher):
    def handle(self, response):
        value = ElementDispatcher.handle(self, response)

        if value:
            return value

        return response
