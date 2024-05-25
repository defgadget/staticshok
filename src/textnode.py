import re

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


def split_nodes_delimiter(
    old_nodes: list[TextNode], delim: str, text_type: str
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        text = node.text
        if not has_open_close_delim(node.text, delim):
            new_nodes.append(node)
            continue

        if text.find(delim) == 0:
            split_text = text.split(delim)
            new_nodes.append(TextNode(split_text[1], text_type))
            new_nodes.append(TextNode(f"{split_text[2]}", text_type_text))
            continue

        if text.rfind(delim) == len(text) - 1:
            split_text = text.split(delim)
            new_nodes.append(TextNode(f"{split_text[0]}", text_type_text))
            new_nodes.append(TextNode(split_text[1], text_type))
            continue

        split_text = text.split(delim)
        new_nodes.append(TextNode(f"{split_text[0]}", text_type_text))
        new_nodes.append(TextNode(split_text[1], text_type))
        new_nodes.append(TextNode(f"{split_text[2]}", text_type_text))

    return new_nodes


def has_open_close_delim(text: str, delim: str) -> bool:
    return text.count(delim) == 2


def extract_markdown_images(text: str) -> list[tuple] | list[None]:
    expr = re.compile(r"!\[(.*?)\]\((.*?)\)")
    image_alt_text = re.findall(expr, text)
    return image_alt_text


def extract_markdown_links(text: str) -> list[tuple] | list[None]:
    expr = re.compile(r"\[(.*?)\]\((.*?)\)")
    links_anchor_url = re.findall(expr, text)
    return links_anchor_url


# look at text for images
# if images exist
# extract images alt and link
# somhow split text on image_text and maintain correct order of original text
### Could find substring of each image_text to determine order?
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        txt = node.text
        images = extract_markdown_images(txt)
        if images:
            for alt_text, img_url in images:
                img = f"![{alt_text}]({img_url})"

                img_idx = txt.find(img)
                img_node = TextNode(alt_text, text_type_image, img_url)

                if img_idx == 0:
                    new_nodes.append(img_node)
                else:
                    text_to_strip = txt[:img_idx]
                    text_node = TextNode(text_to_strip, text_type_text)
                    new_nodes.extend([text_node, img_node])
                txt = txt[img_idx + len(img) :]
        else:
            new_nodes.append(node)
            continue
        if len(txt) > 0:
            new_nodes.append(TextNode(txt, text_type_text))
    return new_nodes


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        txt = node.text
        links = extract_markdown_links(txt)
        if links:
            for anchor_text, link_url in links:
                link = f"[{anchor_text}]({link_url})"

                link_idx = txt.find(link)
                link_node = TextNode(anchor_text, text_type_link, link_url)

                if link_idx == 0:
                    new_nodes.append(link_node)
                else:
                    text_to_strip = txt[:link_idx]
                    text_node = TextNode(text_to_strip, text_type_text)
                    new_nodes.extend([text_node, link_node])
                txt = txt[link_idx + len(link) :]
        else:
            new_nodes.append(node)
            continue
        if len(txt) > 0:
            new_nodes.append(TextNode(txt, text_type_text))
    return new_nodes


def text_to_textnodes(text) -> list[TextNode]:
    seed = TextNode(text, text_type_text)
    text_nodes = split_nodes_delimiter([seed], "**", text_type_bold)
    text_nodes = split_nodes_delimiter(text_nodes, "*", text_type_italic)
    text_nodes = split_nodes_delimiter(text_nodes, "`", text_type_code)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_links(text_nodes)
    return text_nodes


def markdown_to_blocks(text: str) -> list[str]:
    blocks = text.splitlines(True)
    new_nodes = []
    block_str = ""
    for block in blocks:
        if block == "\n":
            if len(block_str) > 0:
                new_nodes.append(block_str)
                block_str = ""
        else:
            block_str += block
    new_nodes.append(block_str)
    return new_nodes
