import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(None, None, None, {'href': "http://www.boot.dev"})
        self.assertEqual(node1.props_to_html(), " href=\"http://www.boot.dev\"")

    def test_props_to_html_2(self):
        node1 = HTMLNode(None, None, None, {"name": "test", "href": "http://www.boot.dev"})
        self.assertEqual(node1.props_to_html(), " href=\"http://www.boot.dev\" name=\"test\"")

    def test_props_to_html_bad_order(self):
        node1 = HTMLNode(None, None, None, {"name": "test", "href": "http://www.boot.dev"})
        node2 = HTMLNode(None, None, None, {"href": "http://www.boot.dev", "name": "test"})
        self.assertEqual(node1.props_to_html(), node2.props_to_html())

        self.assertNotEqual(node1.props_to_html(), " name=\"test\" href=\"http://www.boot.dev\"")
