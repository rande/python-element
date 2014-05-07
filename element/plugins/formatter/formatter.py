import markdown
from docutils.core import publish_parts

class Formatter(object):

    def format(self, content, formatter='markdown'):

        if formatter == 'markdown':
            return markdown.markdown(content, ['tables', 'codehilite', 'fenced_code'])

        elif formatter in ['rst', 'sphinx']:
            parts = publish_parts(content, writer_name='html', settings_overrides={
                'input_encoding': 'unicode',
                'output_encoding': 'unicode',
                'syntax_highlight': 'short',
            })

            return parts['html_body']

        return content