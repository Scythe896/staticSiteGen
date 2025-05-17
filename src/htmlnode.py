class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        # tag = A string for the HTML tag
        # value = A raw text string
        # children = A list of child objects
        # props = A dictionairy of attributes
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        # returns ' key="value"'
        if self.props == None:
            return ""
        res = ""
        for k, v in self.props.items():
            res += f' {k}="{v}"'
        return res

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode: Missing Value")
        if self.tag == None:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.children}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode: Missing Tag")
        if self.children == None:
            raise ValueError("ParentNode: Missing Children")
        res = ""
        for child in self.children:
            res += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{res}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"