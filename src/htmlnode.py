class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props}, {self.children})"

    def to_html(self) -> str:
        return ""

    def props_to_html(self):
        props = ""
        if props == None:
            return props

        if self.props:
            for k, v in self.props.items():
                props += f' {k}: "{v}"'
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


def text_node_to_html_node(text_node) -> HTMLNode:
    tag = ""
    value = text_node.text_type
    props = None
    match text_node.text_type:
        case "text":
            tag = "p"
        case "bold":
            tag = "b"
        case "italic":
            tag = "italic"
        case "code":
            tag = "code"
        case "link":
            tag = "a"
            props = {"href": text_node.url}
        case "image":
            tag = "img"
            value = ""
            props = {"src": text_node.url, "alt": text_node.text}
        case _:
            raise ValueError("unknown TextNode text type: ", text_node.text_type)

    return LeafNode(tag, value, props)
