import os
import element.loaders

class StaticNodeLoader(element.loaders.NodeLoader):
    """
    Load a node from a static file
    """
    def __init__(self, mimetypes):
        self.mimetypes = mimetypes

    def supports(self, path):
        if isinstance(path, dict):
            return 'type' in path and path['type'] == 'element.static'

        filename, extension = os.path.splitext(path)

        return extension[1:] in self.mimetypes

    def load(self, path):
        filename, extension = os.path.splitext(path)

        return {
            'type':      'element.static',
            'file':      path,
            'title':     filename,
            'extension': extension[1:],
            'mimetype':  self.mimetypes[extension[1:]],
            'content':   False
        }

    def save(self, path, data):
        fp = file(path, 'wb')
        fp.write(data['content'])
        fp.flush()
        fp.close()

        return os.path.isfile(path)