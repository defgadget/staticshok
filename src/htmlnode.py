import os


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other) -> bool:
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props}, {self.children})"

    def to_html(self) -> str:
        raise NotImplemented

    def props_to_html(self):
        props = ""
        if props == None:
            return props

        if self.props:
            for k, v in self.props.items():
                props += f' {k}= "{v}"'
        return props


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("leaf node must have value")
        if self.tag is None:
            return self.value

        props = self.props_to_html()
        html = f"<{self.tag}{props}>{self.value}</{self.tag}>"
        return html


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("parent node must have a tag")
        if self.children is None:
            raise ValueError("parent node requires children")

        html = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            html += node.to_html()
        html += f"</{self.tag}>"

        return html
