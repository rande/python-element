
class ProxyStaticMethod(object):
    def __init__(self, types):
        self.types = types

    def is_image(self, node):
        return node.extension.lower() in self.types['image']

    def is_video(self, node):
        return node.extension.lower() in self.types['video']

    def is_document(self, node):
        return node.extension.lower() in self.types['document']

class ProxyMediasMethod(object):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def __call__(self, node, *args, **kwargs):
        """
        Return the list of media for the related media
        """
        return self.node_manager.get_nodes(**{
            'type': 'element.static',
            'path': node.id
        })

class MediaListener(object):
    def __init__(self, proxy_media_method, proxy_static_method):
        self.proxy_media_method = proxy_media_method
        self.proxy_static_method = proxy_static_method

    def add_methods(self, event):
        if event.has('node'):
            nodes = [event.get('node')]
        else:
            nodes = event.get('nodes')

        for node in nodes:
            if node.type == "media.gallery":
                self.add_methods_to_gallery(node)

            if node.type == "element.static":
                self.add_methods_to_static(node)

    def add_methods_to_static(self, node):
        node.methods['is_image'] = self.proxy_static_method.is_image
        node.methods['is_video'] = self.proxy_static_method.is_video
        node.methods['is_document'] = self.proxy_static_method.is_document

    def add_methods_to_gallery(self, node):
        # append functions
        node.methods['medias'] = self.proxy_media_method

        # normalize required parameters
        if not node.parameters:
            node.parameters = {}

        if 'types' not in node.parameters:
            node.parameters['types'] = ['png', 'jpg', 'gif']

        if 'format' not in node.parameters:
            node.parameters['format'] = 'small'