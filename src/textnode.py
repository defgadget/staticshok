text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(old_nodes, delim, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        split_nodes = node.split(delim)
        if len(split_nodes) != 3:
            raise Exception(
                "it looks like your missing the closing delim in -- ", node.text
            )
        new_nodes.append(TextNode(split_nodes[0], text_type_text))
        new_nodes.append(TextNode(f" {split_nodes[1]} ", text_type))
        new_nodes.append(TextNode(split_nodes[2], text_type_text))

    return new_nodes
