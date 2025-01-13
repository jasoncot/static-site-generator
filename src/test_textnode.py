import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC, "http://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_explicit_none(self):
        node = TextNode("This is a text node", TextType.ITALIC, None)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()