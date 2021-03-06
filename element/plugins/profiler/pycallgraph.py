#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import, division

from .collector import BaseCollector

from pycallgraph import PyCallGraph, Config, GlobbingFilter
from pycallgraph.metadata import __version__
from pycallgraph.color import Color
from pycallgraph.output import Output, GraphvizOutput

import os
import textwrap

class DotGraphvizOutput(Output):
    """
    Generates
    """
    def __init__(self, **kwargs):
        self.output_file = 'pycallgraph.dot'
        self.font_name = 'Verdana'
        self.font_size = 7
        self.group_font_size = 10
        self.group_border_color = Color(0, 0, 0, 0.8)

        Output.__init__(self, **kwargs)

        self.prepare_graph_attributes()

    def prepare_graph_attributes(self):
        generated_message = '\\n'.join([
            r'Generated by Python Call Graph v%s' % __version__,
            r'http://pycallgraph.slowchop.com',
        ])

        self.graph_attributes = {
            'graph': {
                'overlap': 'scalexy',
                'fontname': self.font_name,
                'fontsize': self.font_size,
                'fontcolor': Color(0, 0, 0, 0.5).rgba_web(),
                'label': generated_message,
            },
            'node': {
                'fontname': self.font_name,
                'fontsize': self.font_size,
                'fontcolor': Color(0, 0, 0).rgba_web(),
                'style': 'filled',
                'shape': 'rect',
            },
            'edge': {
                'fontname': self.font_name,
                'fontsize': self.font_size,
                'fontcolor': Color(0, 0, 0).rgba_web(),
            }
        }

    def done(self):
        source = self.generate()

        self.debug(source)

        with open(self.output_file, 'w') as f:
            f.write(source)

    def generate(self):
        '''Returns a string with the contents of a DOT file for Graphviz to
        parse.
        '''
        indent_join = '\n' + ' ' * 12

        return textwrap.dedent('''\
        digraph G {{

            // Attributes
            {}

            // Groups
            {}

            // Nodes
            {}

            // Edges
            {}

        }}
        '''.format(
            indent_join.join(self.generate_attributes()),
            indent_join.join(self.generate_groups()),
            indent_join.join(self.generate_nodes()),
            indent_join.join(self.generate_edges()),
        ))

    def attrs_from_dict(self, d):
        output = []
        for attr, val in d.iteritems():
            output.append('%s = "%s"' % (attr, val))
        return ', '.join(output)

    def node(self, key, attr):
        return '"{}" [{}];'.format(
            key, self.attrs_from_dict(attr),
        )

    def edge(self, edge, attr):
        return '"{0.src_func}" -> "{0.dst_func}" [{1}];'.format(
            edge, self.attrs_from_dict(attr),
        )

    def generate_attributes(self):
        output = []
        for section, attrs in self.graph_attributes.iteritems():
            output.append('{} [ {} ];'.format(
                section, self.attrs_from_dict(attrs),
            ))
        return output

    def generate_groups(self):
        if not self.processor.config.groups:
            return ''

        output = []
        for group, nodes in self.processor.groups():
            funcs = [node.name for node in nodes]
            funcs = '" "'.join(funcs)
            group_color = self.group_border_color.rgba_web()
            group_font_size = self.group_font_size
            output.append(
                'subgraph "cluster_{group}" {{ '
                '"{funcs}"; '
                'label = "{group}"; '
                'fontsize = "{group_font_size}"; '
                'fontcolor = "black"; '
                'style = "bold"; '
                'color="{group_color}"; }}'.format(**locals()))
        return output

    def generate_nodes(self):
        output = []
        for node in self.processor.nodes():
            attr = {
                'color': self.node_color_func(node).rgba_web(),
                'label': self.node_label_func(node),
            }
            output.append(self.node(node.name, attr))

        return output

    def generate_edges(self):
        output = []

        for edge in self.processor.edges():
            attr = {
                'color': self.edge_color_func(edge).rgba_web(),
                'label': self.edge_label_func(edge),
            }
            output.append(self.edge(edge, attr))

        return output

class PyCallgraphCollector(BaseCollector):
    def __init__(self, output_path):
        self.output_path = output_path

    def on_request(self, request_handler, run):
        filename = "%s/%s/pycallgraph.dot" % (self.output_path, run.id)

        config = Config()
        config.trace_filter = GlobbingFilter(include=[
            'element.*',
            'ioc.*',
        ])

        callgraph = PyCallGraph(output=DotGraphvizOutput(output_file=filename), config=config)
        callgraph.start()

        request_handler.run.add_data('callgraph', callgraph)
        request_handler.run.add_metric('callgraph', True)

    def on_terminate(self, request_handler, run):
        run.get_data('callgraph').done()

    def get_template(self, run):
        # to do: add the d3js code or the png view ...
        return False