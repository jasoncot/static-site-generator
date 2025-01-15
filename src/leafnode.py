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
