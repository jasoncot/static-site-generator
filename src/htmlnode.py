from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        
        keys = list(self.props.keys())
        keys.sort()

        return reduce(
            lambda acc, key: acc + f" {key}=\"{self.props[key]}\"",
            keys,
            ""
        )
    
    def __repr__(self):
        return f"HTMLNode(tag: \"{self.tag}\", value: \"{self.value}\", children: \"{self.children}\", props: \"{self.props}\")"
