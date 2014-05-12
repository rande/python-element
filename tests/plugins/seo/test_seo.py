# vim: set fileencoding=utf-8 :
import unittest

from element.plugins.seo import SeoListener, SeoPage
from element.node import Node
from element.node import NodeContext

from ioc.event import Event

class SeoListenerTest(unittest.TestCase):
    def test_title(self):
        page = SeoPage()
        listener = SeoListener(page)

        self.assertEquals("title", listener.get_title("title"))

    def test_event_without_subject(self):
        event = Event()

        SeoListener(SeoPage()).listener(event)

        self.assertFalse(event.has('node'))

    def test_event_with_subject(self):

        event = Event({
            'subject': NodeContext(Node())
        })

        SeoListener(SeoPage()).listener(event)

        self.assertTrue(event.has('node'))

        node = event.get('node')
        self.assertEquals(node.seo['title'], u"\u2605")
        self.assertEquals(node.seo['metas'], {})

    def test_event_with_subject_seo(self):
        event = Event({
            'subject': NodeContext(Node(), {
                'name': 'the name',
                'seo': {
                    'metas': {
                        'name': {
                            'keywords': 'list, of, keywords'
                        }
                    }
                }
            })
        })

        SeoListener(SeoPage("site - %s", {
            'name': {
                'description': 'The description'
            }
        })).listener(event)

        self.assertTrue(event.has('node'))

        node = event.get('node')
        self.assertEquals(node.seo['title'], "site - the name")
        self.assertEquals(node.seo['metas'], {
            'name': {
                'keywords': 'list, of, keywords',
                'description': 'The description'
            }
        })