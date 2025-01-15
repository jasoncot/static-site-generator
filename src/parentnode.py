from htmlnode import HTMLNode
from textnode import TextNode, TextType

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("tag is required")
        
        if self.children == None:
            raise ValueError("children is required")
        
        def handle_child_to_html(node):
            if isinstance(node, TextNode):
                if node.text_type != TextType.TEXT:
                    raise Exception(f"unable to handle {node.text_type} TextNode")
                return node.text
            if isinstance(node, HTMLNode):
                return node.to_html()
            
            raise Exception("unknown node type being converted to html")

        children_values = "".join(list(map(
            handle_child_to_html,
            self.children
        )))
        
        return f"<{self.tag}{self.props_to_html()}>{children_values}</{self.tag}>"