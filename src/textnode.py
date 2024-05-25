from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text: str, text_type: str, url: str = "") -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node) -> LeafNode:
    tag = ""
    value = text_node.text
    props = None
    match text_node.text_type:
        case "text":
            tag = None
        case "bold":
            tag = "b"
        case "italic":
            tag = "i"
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
