import unittest
from leafnode import LeafNode
from textnode import TextType, TextNode

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

    def test_text_node_convert(self):
        text_node = TextNode("text node", TextType.TEXT, None)
        leaf_node = LeafNode.text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), "text node")

    def test_normal_node_convert(self):
        text_node = TextNode("text node", TextType.NORMAL, None)
        leaf_node = LeafNode.text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), "text node")

    def test_bold_node_convert(self):
        text_node = TextNode("text node", TextType.BOLD, None)
        leaf_node = LeafNode.text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), "<b>text node</b>")

    def test_italic_node_convert(self):
        text_node = TextNode("text node", TextType.ITALIC, None)
        leaf_node = LeafNode.text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), "<i>text node</i>")

    def test_code_node_convert(self):
        text_node = TextNode("text node", TextType.CODE, None)
        leaf_node = LeafNode.text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), "<code>text node</code>")

    def test_link_node_convert(self):
        text_node = TextNode("text node", TextType.LINK, "http://www.google.com")
        leaf_node = LeafNode.text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), "<a href=\"http://www.google.com\">text node</a>")

    def test_image_node_convert(self):
        text_node = TextNode("text node", TextType.IMAGE, "http://www.google.com")
        leaf_node = LeafNode.text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), "<img alt=\"text node\" src=\"http://www.google.com\">")