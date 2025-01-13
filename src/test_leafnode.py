import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node1.to_html(), "<p>This is a paragraph of text.</p>")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_to_html_no_tag(self):
        node1 = LeafNode(None, "This is just text in a text node")
        self.assertEqual(node1.to_html(), "This is just text in a text node")

    def test_to_html_no_tag_with_props(self):
        node1 = LeafNode(None, "This is just text in a text node", {"href": "https://www.google.com"})
        self.assertEqual(node1.to_html(), "This is just text in a text node")
