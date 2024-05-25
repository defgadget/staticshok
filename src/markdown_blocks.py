from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered list"


def block_to_block_type(block: str) -> str:
    lines = block.splitlines()
    if block.startswith(
        (
            "# ",
            "## ",
            "### ",
            "#### ",
            "##### ",
            "###### ",
        )
    ):
        return block_type_heading
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith(("- ", "* ")):
        line_start = block[:2]
        for line in lines:
            if line[:2] != line_start:
                return block_type_paragraph
        return block_type_unordered_list
    if block.startswith("1. "):
        count = 1
        for line in lines:
            if not line.startswith(f"{count}. "):
                return block_type_paragraph
            count += 1
        return block_type_ordered_list
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    return block_type_paragraph


def markdown_to_html_node(document: str) -> ParentNode:
    blocks = markdown_to_blocks(document)
    children = []
    for block in blocks:
        html = block_to_html_node(block)
        children.append(html)
    return ParentNode("div", children, None)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_block_to_html(block)
    if block_type == block_type_heading:
        return heading_block_to_html(block)
    if block_type == block_type_code:
        return code_block_to_html(block)
    if block_type == block_type_quote:
        return quote_block_to_html(block)
    if block_type == block_type_unordered_list:
        return unord_list_block_to_html(block)
    if block_type == block_type_ordered_list:
        return ord_list_block_to_html(block)
    raise Exception("unkown block type")


def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html = text_node_to_html_node(node)
        children.append(html)
    return children


def paragraph_block_to_html(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_block_to_html(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 > len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_block_to_html(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def quote_block_to_html(block: str) -> ParentNode:
    lines = block.splitlines()
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unord_list_block_to_html(block: str) -> ParentNode:
    lines = block.splitlines()
    html_items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def ord_list_block_to_html(block: str) -> ParentNode:
    lines = block.splitlines()
    html_items = []
    count = 1
    for line in lines:
        token = f"{count}. "
        text = line[len(token) :]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
        count += 1
    return ParentNode("ol", html_items)


def markdown_to_blocks(text: str) -> list[str]:
    blocks = text.split("\n\n")
    new_nodes = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        if block.endswith("\n"):
            print("ends with new line")
        new_nodes.append(block)
    return new_nodes
