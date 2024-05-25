import os

from blocknode import (
    BlockNode,
    block_to_block_type,
    block_type_code,
    block_type_heading,
    block_type_ordered_list,
    block_type_paragraph,
    block_type_quote,
    block_type_unordered_list,
)
from textnode import markdown_to_blocks


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


def markdown_to_html(document: str) -> HTMLNode:
    blocks = markdown_to_blocks(document)
    typed_blocks = []
    for block in blocks:
        typed_blocks.append(block_to_block_type(block))

    children = []
    for block in typed_blocks:
        match block.block_type:
            case "paragraph":
                children.append(paragraph_block_to_html(block))
            case "heading":
                children.append(heading_block_to_html(block))
            case "code":
                children.append(code_block_to_html(block))
            case "quote":
                children.append(quote_block_to_html(block))
            case "unordered list":
                children.append(unord_list_block_to_html(block))
            case "ordered list":
                children.append(ord_list_block_to_html(block))
            case _:
                raise Exception("unkown block type")
    return ParentNode("div", children)


def paragraph_block_to_html(block: BlockNode) -> HTMLNode:
    return LeafNode("p", block.block)


def heading_block_to_html(block: BlockNode) -> HTMLNode:
    count = block.block.count("#", 0, 6)
    heading = f"h{count}"
    return LeafNode(heading, block.block)


def code_block_to_html(block: BlockNode) -> HTMLNode:
    return ParentNode("pre", [LeafNode("code", block.block)])


def quote_block_to_html(block: BlockNode) -> HTMLNode:
    return LeafNode("blockquote", block.block)


def unord_list_block_to_html(block: BlockNode) -> HTMLNode:
    lines = block.block.splitlines()
    children = []
    for line in lines:
        children.append(LeafNode("li", line))
    return ParentNode("ul", children)


def ord_list_block_to_html(block: BlockNode) -> HTMLNode:
    lines = block.block.splitlines()
    children = []
    for line in lines:
        children.append(LeafNode("li", line))
    return ParentNode("ol", children)


def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line
    raise Exception("no header in this file")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as from_file:
        from_contents = from_file.read()

    with open(template_path) as template_file:
        template_contents = template_file.read()

    title = extract_title(from_contents)
    contents = markdown_to_html(from_contents).to_html()

    template_contents.replace("{{ Title }}", title)
    template_contents.replace("{{ Content }}", contents)

    dirs = os.path.dirname(dest_path)
    os.makedirs(dirs, exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(template_contents)
