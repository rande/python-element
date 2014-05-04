import markdown
from docutils.core import publish_parts

class Formatter(object):

    def format(self, content, formatter='markdown'):

        if formatter == 'markdown':
            return markdown.markdown(content, ['tables'])

        elif formatter in ['rst', 'sphinx']:
            return publish_parts(content, writer_name='html')['html_body']

        return content