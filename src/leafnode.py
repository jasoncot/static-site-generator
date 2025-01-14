from htmlnode import HTMLNode
from textnode import TextType, TextNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None or self.value == "":
            raise ValueError()
        
        if self.tag == None:
            return self.value
        if self.tag == "img":
            self.props["alt"] = self.value
            return f"<{self.tag}{self.props_to_html()}>"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        

    def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        
        if text_node.text_type == TextType.NORMAL:
            return LeafNode(None, text_node.text)
        
        if text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text)
        
        if text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text)
        
        if text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text)
        
        if text_node.text_type == TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})

        if text_node.text_type == TextType.IMAGE:
            return LeafNode("img", text_node.text, {"src": text_node.url})
        
        raise Exception("unknown text_node type")