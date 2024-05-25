block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered list"


class BlockNode:
    def __init__(self, block: str, block_type: str) -> None:
        self.block = block
        self.block_type = block_type

    def __eq__(self, other) -> bool:
        return self.block == other.block and self.block_type == other.block_type

    def __repr__(self) -> str:
        return f"BlockNode({self.block}, {self.block_type})"


def block_to_block_type(block: str) -> BlockNode:
    if block == "" or block == None:
        raise Exception("Something went wrong")
    lines = block.splitlines()

    is_heading = False
    is_unord_list = False
    is_ord_list = False
    is_code = False
    is_quote = False

    if block[0] == "#":
        count = 1
        for i in range(1, len(block)):
            if block[i] == " " and count < 6:
                is_heading = True
            elif block[i] == "#":
                count += 1
            else:
                break
    elif block[0] == ">":
        is_quote = True
        for line in lines:
            if line[0] != ">":
                is_quote = False
                break
    elif block[:2] == "- " or block[:2] == "* ":
        line_start = block[:2]
        is_unord_list = True
        for line in lines:
            if line[:2] != line_start:
                is_unord_list = False
                break
    elif block[:2] == "1.":
        is_ord_list = True
        count = 1
        for line in lines:
            if line[:2] != f"{count}.":
                is_ord_list = False
                break
            count += 1
    elif block[:3] == "```":
        if block[-3:]:
            is_code = True

    node = None
    if is_heading:
        node = BlockNode(block, block_type_heading)
    elif is_unord_list:
        node = BlockNode(block, block_type_unordered_list)
    elif is_ord_list:
        node = BlockNode(block, block_type_ordered_list)
    elif is_code:
        node = BlockNode(block, block_type_code)
    elif is_quote:
        node = BlockNode(block, block_type_quote)
    else:
        node = BlockNode(block, block_type_paragraph)

    return node
