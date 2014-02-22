import random, yaml
from start import get_container
import os, logging
import sys

"""
This script must by the wsgi handler to start the application. 

You can customize it for your need.
"""
base = sys.path[0]
sys.path.insert(0, base + "/../../../")

from element.node import Node


debug = True

# if debug:
#     logging.basicConfig(level=logging.DEBUG)

parameters = {
    'ioc.debug': debug,
    'ioc.env': 'prod',
    'project.root_folder': os.path.dirname(os.path.realpath(__file__))
}


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


container = get_container(parameters)

mongo = container.get('element.manager.mongodb')


def clean(mongo):
    print "Removing data"
    mongo.get_collection().remove()

def insert_posts(mongo):
    print "Inserting Posts"
    count = 0

    root = mongo.save(None, "core.node", {
        "parent": None,
        "slug": "blog"
    })

    for year in range(2012, 2013):

        node_year = mongo.save(None, "core.node", {
            "parent": root['id'],
            "slug": year
        })

        for month in range(1, 12):
            node_month = mongo.save(None, "core.node", {
                "parent": node_year['id'],
                "slug": month
            })

            for pos in range(1, 100):
                if count % 500 == 0:
                    print count

                count += 1
                # print node
                print mongo.save(None, "blog.post", {
                    "parent": node_month['id'],
                    'type': 'blog.post',
                    'title': "Blog post demo test %s/%02d/%03d" % (year, month, pos),
                    'category': random.choice(categories),
                    'tags': random.sample(tags, random.randint(0, 6)),
                    'content': content,
                    'format': 'markdown',
                    'slug': 'blog-post-demo-test-%s-%02d-%03d' % (year, month, pos)
                })


    print "Inserting %s Posts, done!" % count

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


clean(mongo)
#insert_medias(mongo)
insert_posts(mongo)
