from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("tag is required")
        
        if self.children == None:
            raise ValueError("children is required")
        
        children_values = "".join(list(map(
            lambda child: child.to_html(),
            self.children
        )))
        
        return f"<{self.tag}{self.props_to_html()}>{children_values}</{self.tag}>"