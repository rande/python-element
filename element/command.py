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

from ioc.extra.command import Command
import random

class ListTypeCommand(Command):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def initialize(self, parser):
        parser.description = "List node types available"

    def execute(self, args, output):
        output.write("Nodes type available:\n")

        for name, service in self.node_manager.handlers.iteritems():
            output.write(" - %s \n" % name)

        output.write("\n--\nPython Element - Thomas Rabaix <thomas.rabaix@gmail.com>\n")


class LoadDemoFixtureCommand(Command):
    def __init__(self, mongo):
        self.mongo = mongo

    def initialize(self, parser):
        parser.description = "Erase database and load demo fixtures"

    def execute(self, args, output):

        tags = ['python', 'element', 'test', 'stress', 'requests', 'jinja', 'ioc']
        categories = ['world', 'france', 'uk', 'usa', 'germany', 'spain', 'italy']

        content = """
**Nullam lacinia ante justo**. Aliquam consectetur semper magna, in imperdiet ligula posuere vel.
Ut ut nulla tortor. Integer laoreet tellus id mi feugiat et bibendum dolor iaculis. Phasellus
id quam quis tortor interdum venenatis eu eget lacus. Aenean a magna non risus lobortis
sollicitudin eget quis odio. Proin at turpis augue, a dignissim sapien. Duis eget sem sit
amet urna hendrerit semper. Nulla facilisi. Nunc molestie facilisis tellus. Quisque eget
volutpat magna. Integer nec facilisis est.

Etiam dapibus dui non ante imperdiet ut pharetra lorem blandit. Vivamus sit amet laoreet augue.
Pellentesque eu ipsum non nunc porttitor pharetra. Pellentesque in dui massa. Sed venenatis
lectus id arcu sagittis pharetra. Donec porttitor justo vel arcu posuere gravida non nec est.
Suspendisse ornare tempus sapien at fermentum. Phasellus ultrices venenatis eros sed convallis.
Nullam bibendum laoreet orci eu vestibulum. Praesent sagittis, massa sed pharetra pulvinar,
diam dui semper lacus, vel ornare diam ipsum sit amet nunc. Pellentesque eu rutrum erat.
Suspendisse eu scelerisque velit. Integer ac mi quam, vitae convallis lacus.

**Nullam lacinia ante justo**. Aliquam consectetur semper magna, in imperdiet ligula posuere vel.
Ut ut nulla tortor. Integer laoreet tellus id mi feugiat et bibendum dolor iaculis. Phasellus
id quam quis tortor interdum venenatis eu eget lacus. Aenean a magna non risus lobortis
sollicitudin eget quis odio. Proin at turpis augue, a dignissim sapien. Duis eget sem sit
amet urna hendrerit semper. Nulla facilisi. Nunc molestie facilisis tellus. Quisque eget
volutpat magna. Integer nec facilisis est.

Etiam dapibus dui non ante imperdiet ut pharetra lorem blandit. Vivamus sit amet laoreet augue.
Pellentesque eu ipsum non nunc porttitor pharetra. Pellentesque in dui massa. Sed venenatis
lectus id arcu sagittis pharetra. Donec porttitor justo vel arcu posuere gravida non nec est.
Suspendisse ornare tempus sapien at fermentum. Phasellus ultrices venenatis eros sed convallis.
Nullam bibendum laoreet orci eu vestibulum. Praesent sagittis, massa sed pharetra pulvinar,
diam dui semper lacus, vel ornare diam ipsum sit amet nunc. Pellentesque eu rutrum erat.
Suspendisse eu scelerisque velit. Integer ac mi quam, vitae convallis lacus.

**Nullam lacinia ante justo**. Aliquam consectetur semper magna, in imperdiet ligula posuere vel.
Ut ut nulla tortor. Integer laoreet tellus id mi feugiat et bibendum dolor iaculis. Phasellus
id quam quis tortor interdum venenatis eu eget lacus. Aenean a magna non risus lobortis
sollicitudin eget quis odio. Proin at turpis augue, a dignissim sapien. Duis eget sem sit
amet urna hendrerit semper. Nulla facilisi. Nunc molestie facilisis tellus. Quisque eget
volutpat magna. Integer nec facilisis est.

Etiam dapibus dui non ante imperdiet ut pharetra lorem blandit. Vivamus sit amet laoreet augue.
Pellentesque eu ipsum non nunc porttitor pharetra. Pellentesque in dui massa. Sed venenatis
lectus id arcu sagittis pharetra. Donec porttitor justo vel arcu posuere gravida non nec est.
Suspendisse ornare tempus sapien at fermentum. Phasellus ultrices venenatis eros sed convallis.
Nullam bibendum laoreet orci eu vestibulum. Praesent sagittis, massa sed pharetra pulvinar,
diam dui semper lacus, vel ornare diam ipsum sit amet nunc. Pellentesque eu rutrum erat.
Suspendisse eu scelerisque velit. Integer ac mi quam, vitae convallis lacus.
"""

        self.clean()

        output.write("Inserting Posts\n")
        count = 0

        root = self.mongo.save(None, {
            "parent": None,
            "slug": "blog",
            "type": "core.node"
        })

        for year in range(2012, 2013):
            node_year = self.mongo.save(None, {
                "parent": root['uuid'],
                "slug": year,
                "type": "core.node"
            })

            for month in range(1, 12):
                node_month = self.mongo.save(None, {
                    "parent": node_year['uuid'],
                    "slug": month,
                    "type": "core.node"
                })

                for pos in range(1, 100):
                    if count % 500 == 0:
                        output.write("write %s elements\n" % count)

                    count += 1
                    # print node
                    self.mongo.save(None, {
                        "parent": node_month['uuid'],
                        'type': 'blog.post',
                        'title': "Blog post demo test %s/%02d/%03d" % (year, month, pos),
                        'category': random.choice(categories),
                        'tags': random.sample(tags, random.randint(0, 6)),
                        'content': content,
                        'format': 'markdown',
                        'slug': 'blog-post-demo-test-%s-%02d-%03d' % (year, month, pos)
                    })


        output.write("Inserting %s Posts, done! \n" % count)

    def clean(self):
        self.mongo.get_collection().remove()

    #def insert_medias(manager):
    #    print "Inserting Medias"
    #    count = 0
    #    for years in range(2012, 2013):
    #        for month in range(1, 12):
    #            for pos in range(1, 100):
    #                data = {
    #                    'alias': "medias/%s-%02d-%03d.bin" % (years, month, pos),
    #                    'type': 'element.static',
    #                    'title': "The media %s-%02d-%03d" % (years, month, pos),
    #                    'category': random.choice(categories),
    #                    'tags': random.sample(tags, random.randint(0, 6)),
    #                    'content': content,
    #                    'manager': 'mongodb',
    #                }
    #
    #                if count % 500 == 0:
    #                    print count
    #
    #                count += 1
    #                # print node
    #                node = Node(None, 'element.static', data, 'mongodb')
    #
    #                manager.save(node)
    #
    #    print "Inserting Medias %s done!" % count
    #
